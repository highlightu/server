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
from django.conf.urls import include  # url뿐 아니라 include를 import해야 합니다.
from django.contrib import admin
from django.urls import path
from main.views import *  # 1st app : main homepage
from django.conf.urls.static import static

urlpatterns = [
    # base
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    #path('mypage/', include('dashboard.urls')),
    #path('mypage/dashboard/', include('upload.urls')),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
