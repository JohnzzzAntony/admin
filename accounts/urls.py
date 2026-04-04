from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('guest-checkout/', views.guest_checkout_view, name='guest_checkout'),
    path('social/<str:provider>/', views.social_login, name='social_login'),
    path('callback/', views.social_callback, name='social_callback'),
]
