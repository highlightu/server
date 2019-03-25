"""django_capstone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url, include  # url뿐 아니라 include를 import해야 합니다.
from django.conf import settings
from django.contrib import admin
from django.urls import path
from user_management.views import *

SOCIAL_AUTH_URL_NAMESPACE = 'social'

LOGIN_REDIRECT_URL = '/'

urlpatterns = [
    # base
    path('admin/', admin.site.urls),

    # first ui
    path('', social_login),

    # authentication with google
    path('oauth/', include('social_django.urls', namespace='social')),

    # success
    path('home/', home),

    # logout
    path('logout/', logout, name='logout'),
]
