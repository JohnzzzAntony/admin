from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about-us/', views.about_us_view, name='about_us'),
    path('services/', views.services_view, name='services'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('store-locations/', views.store_locations_view, name='store_locations'),
]
