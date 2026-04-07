import os
import json
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from products.models import Category, Product, ProductSKU, ProductImage
from django.utils.text import slugify
from django.conf import settings
from decimal import Decimal

import google.generativeai as genai

@staff_member_required
def ai_dashboard(request):
    """
    Renders the AI Store Manager dashboard.
    """
    return render(request, 'ai_manager/dashboard.html')


@csrf_exempt
def ai_process_command(request):
    """
    Advanced API endpoint that uses Google Gemini to process natural language 
    commands into actionable backend store operations.
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'status': 'error', 'message': 'Authentication required. Please log in as a staff member.'}, status=403)
        
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)
        
    try:
        data = json.loads(request.body)
        user_prompt = data.get('prompt', '')
        
        # --- Late-Binding Gemini Core ---
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not gemini_api_key:
            return JsonResponse({
                'status': 'error', 
                'message': 'Gemini AI Engine is not configured. GEMINI_API_KEY is missing from environment.'
            }, status=500)

        genai.configure(api_key=gemini_api_key)
        try:
            # Using -latest as an alias for stability across different library versions
            gemini_client = genai.GenerativeModel('gemini-1.5-flash-latest')
        except:
            # Fallback to the rock-solid gemini-pro
            gemini_client = genai.GenerativeModel('gemini-pro')

        # 🚀 Google Gemini Orchestration
        sys_prompt = (
            "You are the JKR Store Manager AI, a professional autonomous agent. "
            "You help manage an e-commerce store. "
            "IMPORTANT: If the user wants to add or create a category, you MUST start your response with 'ADD_CATEGORY: [Name]'. "
            "If they want to generate an image or visualization, start with 'IMAGE: [Prompt]'. "
            "Otherwise, provide a concise and professional business response."
        )

        config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "max_output_tokens": 1024,
        }
        
        # Call Gemini
        res = gemini_client.generate_content(f"{sys_prompt}\n\nUser Question: {user_prompt}", generation_config=config)
        full_content = res.text
        
        # --- Multi-Path Neural Parsing ---
        
        # 1. Category Creation Path
        if "ADD_CATEGORY:" in full_content:
            category_name = full_content.split("ADD_CATEGORY:")[-1].split("\n")[0].strip().title()
            category_name = category_name.replace("*", "").replace("#", "").strip()
            
            if category_name:
                cat, created = Category.objects.get_or_create(name=category_name)
                response_text = f"📦 **DATABASE SYNC**: Successfully initialized the **{category_name}** category." if created else f"ℹ️ The category **{category_name}** is already active."
                return JsonResponse({'status': 'success', 'response': response_text, 'action': 'create_category'})

        # 2. Image Generation Path
        if "IMAGE:" in full_content:
            image_prompt = full_content.split("IMAGE:")[-1].split("\n")[0].strip()
            return JsonResponse({
                'status': 'success', 
                'response': f"🎨 **NEURAL RENDER INITIATED**: Processing visual generation for: '{image_prompt}'...",
                'action': 'generate_image',
                'meta': {'prompt': image_prompt}
            })

        # 3. Standard Chat Response
        return JsonResponse({'status': 'success', 'response': full_content, 'action': None})
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f"🤖 **AI AGENT ERROR**: {str(e)}"}, status=500)
