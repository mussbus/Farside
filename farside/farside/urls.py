"""
URL configuration for farside project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from user import views as user_views
from django.contrib.auth import views as authentication_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('football/', include('football.urls')),
    path('base/', include('base.urls')),
    path('schedule/', include('schedule.urls')),
    path('register/', user_views.register_view, name='register'),
    path('login/', user_views.login_view, name='login'),
    path('logout/', authentication_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('', user_views.dashboard, name='dashboard')
] 
