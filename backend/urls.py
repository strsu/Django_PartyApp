"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, re_path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('Auth/', include('Auth.urls')),
    re_path('Profile/', include('Profile.urls')),
    re_path('Anony/', include('Anony.urls')),
    re_path('MainParty/', include('mainParty.urls')),
    re_path('SubParty/', include('subParty.urls')),
    re_path('Recommand/', include('Recommand.urls')),
    re_path('Push/', include('Push.urls')),

    re_path('media/', include('media.urls')),
]