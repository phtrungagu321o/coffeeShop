from django.urls import path

from . import views

app_name = 'basket'

urlpatterns = [
    path('', views.basket_summary, name='basket_summary'),
    path('add/', views.basket_add, name='basket_add'),
    path('list_add/', views.basket_list_add, name='basket_list_add'),
    path('list_add/<int:id>', views.basket_list_add_by_id, name='basket_list_add_by_id'),
    path('delete/', views.basket_delete, name='basket_delete'),
    path('update/', views.basket_update, name='basket_update'),
]
