from django.urls import path
from . import views

app_name = 'ai_manager'

urlpatterns = [
    path('dashboard/', views.ai_dashboard, name='ai_dashboard'),
    path('api/process/', views.ai_process_command, name='ai_process_command'),
]
