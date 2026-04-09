from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories/api', views.CategoryViewSet, basename='category_api')

app_name = 'products'

urlpatterns = [
    path('api/', include(router.urls)), # API Endpoints
    path('', views.category_index, name='category_index'),
    path('results/', views.product_list, name='product_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('category/<path:hierarchy_path>/', views.category_detail, name='category_hierarchy_detail'),
    
    # Internal Admin APIs
    path('api/media/delete/<int:pk>/', views.delete_product_media, name='delete_product_media'),
    
    re_path(r'^id/(?P<pk>.*)/$', views.product_detail, name='product_detail'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]
