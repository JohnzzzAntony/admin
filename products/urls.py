from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.category_index, name='category_index'),
    path('results/', views.product_list, name='product_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    
    # Dual-support for both slug and ID-based reversing. 
    # This specifically catches cases in Jazzmin/Admin where it might try 
    # to reverse for a PK before a slug is fully generated or saved.
    re_path(r'^id/(?P<pk>.*)/$', views.product_detail, name='product_detail'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]
