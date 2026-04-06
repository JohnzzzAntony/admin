import os
import json
import openai
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from products.models import Category, Product, ProductSKU, ProductImage
from django.utils.text import slugify
from django.conf import settings
from decimal import Decimal

# --- GPT-4o-mini powered Intelligent Store Manager ---
# This version uses the official OpenAI SDK and handles multi-turn store management tasks.

client = None
if os.getenv('OPENAI_API_KEY'):
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@staff_member_required
def ai_dashboard(request):
    """
    Renders the AI Store Manager dashboard.
    """
    return render(request, 'ai_manager/dashboard.html')

@csrf_exempt
@staff_member_required
def ai_process_command(request):
    """
    Advanced API endpoint that uses OpenAI to process natural language commands 
    into actionable backend store operations.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)
        
    try:
        data = json.loads(request.body)
        user_prompt = data.get('prompt', '')
        
        if not client:
            return JsonResponse({'status': 'error', 'message': 'OpenAI API Key is missing in .env'}, status=500)

        # 🚀 Intelligent Reasoning Engine
        # We define tools for GPT to "call" backend functions
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "create_category",
                    "description": "Create a new product category in the store database.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "The friendly name of the category, e.g. 'Electronics'"}
                        },
                        "required": ["name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "generate_product_image",
                    "description": "Connect to DALL-E to generate a high-quality product visualization.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "description": {"type": "string", "description": "Visual description of the product image to generate"}
                        },
                        "required": ["description"]
                    }
                }
            }
        ]

        messages = [
            {"role": "system", "content": "You are the JKR Store Manager AI. You are autonomous, professional, and helpful. You have access to backend tools to modify the store database. When a user asks to add categories or items, use your tools. If they just want to chat or plan, respond concisely with business insight."},
            {"role": "user", "content": user_prompt}
        ]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        response_message = response.choices[0].message
        
        # --- Handle Function Calling (Neural Link) ---
        if response_message.tool_calls:
            tool_call = response_message.tool_calls[0]
            function_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            
            if function_name == "create_category":
                cat_name = args.get('name', 'New Category').title()
                cat, created = Category.objects.get_or_create(name=cat_name)
                if created:
                    return JsonResponse({
                        'status': 'success', 
                        'response': f"📦 **DATABASE UPDATE**: I have successfully initialized and registered the **{cat_name}** category in your store ecosystem.",
                        'action': 'create_category'
                    })
                return JsonResponse({'status': 'success', 'response': f"ℹ️ The category **{cat_name}** is already indexed and active."})

            if function_name == "generate_product_image":
                desc = args.get('description', '')
                return JsonResponse({
                    'status': 'success', 
                    'response': f"🎨 **NEURAL RENDER INITIATED**: Processing visual generation for: '{desc}'. Connecting to DALL-E 3...",
                    'action': 'generate_image',
                    'meta': {'prompt': desc}
                })

        # Base Chat Response
        return JsonResponse({
            'status': 'success',
            'response': response_message.content,
            'action': None
        })
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
