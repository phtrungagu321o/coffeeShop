from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from . import views
from .forms import (UserLoginForm, PwdResetForm, PwdResetConfirmForm)

app_name = 'account'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html',
                                                form_class=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/account/login/'), name='logout'),
    path('register/', views.account_register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'),
    # reset password
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='account/password_reset/password_reset_form.html',
                                              success_url='password_reset_email_confirm',
                                              email_template_name='account/password_reset/password_reset_email.html',
                                              form_class=PwdResetForm), name='pwdreset'),
    path('password_reset_confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset/password_reset_confirm.html',
                                                     success_url='password_reset_complete/',
                                                     form_class=PwdResetConfirmForm
                                                     ), name='password_reset_confirm'),
    path('password_reset/password_reset_email_confirm/',
         TemplateView.as_view(template_name="account/password_reset/reset_status.html"), name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/password_reset_complete/',
         TemplateView.as_view(template_name='account/password_reset/reset_status.html'),
         name='password_reset_complete'),
    # dashboard dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.edit_details, name='edit_details'),
    path('profile/delete_user/', views.delete_user, name='delete_user'),
    path('profile/delete_confirm/', TemplateView.as_view(template_name='account/dashboard/delete_confirm.html'),
         name='delete_confirm'),

    path("addresses/", views.view_address, name="addresses"),
    path("add_address/", views.add_address, name="add_address"),
    path("addresses/edit/<slug:id>/", views.edit_address, name="edit_address"),
    path("delivery_address/edit/<slug:id>/", views.edit_address, name="edit_address-delivery"),
    path("addresses/delete/<slug:id>/", views.delete_address, name="delete_address"),
    path("addresses/set_default/<slug:id>/", views.set_default, name="set_default"),

    path('wishlist', views.wishlist, name='wishlist'),
    path('wishlist/add_to_wishlist/<int:id>', views.add_to_wishlist, name='user_wishlist'),

    path('save_list/', views.save_list, name='save_list'),
    path('save_list/add_to_wishlist/', views.user_save_list, name='user_save_list'),
    path('save_list/edit_title/<int:id>/', views.edit_title_save, name='edit_title_save'),
    path('save_list/delete_save/<int:id>/', views.delete_save, name='delete_save'),

    path('user_orders/', views.user_orders, name='user_orders'),

    path('user_not_orders/', views.user_not_orders, name='user_not_orders'),

    path("user_not_orders/delete/<int:id>/", views.delete_order, name="delete_order"),

    path('user_orders/rating/<int:id>/', views.rating, name='rating'),
    path('user_orders/rating/<int:id>/<int:rate>', views.rating_ditgis, name='rating_disgis'),

    path('user_orders/val_order/<int:id>/', views.val_order, name='val_order'),

]
