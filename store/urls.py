from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='index'),
    path('search_img/', views.home_img, name='index_img'),
    path('product/', views.product_all, name='product_all'),
    path('<slug:slug>/<int:category_id>/', views.product_detail, name='product_detail'),
    path('shop/<slug:category_slug>/', views.category_list, name='category_list'),
    path('search_result/', views.search, name='search'),
    path('search_result/img', views.search_img, name='search_img'),
    path('display/', views.display, name='display'),
]
