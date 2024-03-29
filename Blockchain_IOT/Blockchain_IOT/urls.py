"""Blockchain_IOT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from Blockchain import views
import re
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = 'home' ),
    url(r'initiate/', views.initiate, name = "initiate" ),
    url(r'block_add/', views.block_add, name = "block_add" ),
    url(r'view_blockchain/', views.view_blockchain, name = "view_blockchain" ),
    url(r'particles/', views.particles, name = "particles"),
]
