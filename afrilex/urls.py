"""afrilex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_view
from .views import (
    home_view, 
    about_view,
    office_view, 
    expert_view, 
    add_profile_view, 
    login_view, 
    signup_view,
    edit_profile_view,
    notifications_view,
    account_view,
    logout_view
)
from searches.views import search_view

urlpatterns = [
    path("", home_view, name="home"),    
    path("about/", about_view, name="about"),
    path("search/", search_view, name="search"),
    path("office/<str:slug>/", office_view, name="office"),
    path("expert/<str:slug>/", expert_view, name="expert"),
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("add-profile/", add_profile_view, name="add-profile"),
    path("update-profile/", edit_profile_view, name="edit-profile"),
    path("account/", account_view, name="account"),
    path("notifications/", notifications_view, name="notifications"),
    path("logout/", logout_view, name="logout"),
    path("reset_password/", 
        auth_view.PasswordResetView.as_view(template_name="password_reset.html"),
        name="reset_password"),
    path("reset_password_sent/", 
        auth_view.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),
        name="password_reset_done"),
    path("reset/<uidb64>/<token>/", 
        auth_view.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),
        name="password_reset_confirm"),
    path("reset_password_complete/", 
        auth_view.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),
        name="password_reset_complete"),
    ### Backend URL
    path('backend/', admin.site.urls, name="backend"),
]

if settings.DEBUG:
    # Test mode
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)