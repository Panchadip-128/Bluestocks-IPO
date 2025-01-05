"""
URL configuration for IPO project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ipo_app.views import stock_list
from ipo_app import views
from django.contrib.auth import views as auth_views
from django.urls import include
from rest_framework.routers import DefaultRouter
from ipo_app.views import dashboard_view

from ipo_app.viewsets import IPOViewSet
# Router for API URLs
router = DefaultRouter()
router.register(r'ipos', IPOViewSet)

# URL Patterns
urlpatterns = [
    # Home and basic app views
    path('', views.home, name='home'), 
    path("admin/", admin.site.urls),
    path('stocks/', stock_list, name='stock_list'),
    path('ipos/', views.list_ipos, name='list_ipos'),
    path('subscribe/<int:ipo_id>/', views.subscribe_to_ipo, name='subscribe'),
    path('transactions/', views.user_transactions, name='transactions'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    
    # Password reset views
    path('forgot_password/', 
         auth_views.PasswordResetView.as_view(template_name='forgot_pw.html'), 
         name='password_reset'),
    path('forgot-password/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), 
         name='password_reset_done'),
    path('reset-password/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), 
         name='password_reset_complete'),
    
    # API routes
    path('api/', include(router.urls)),
]
