from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',views.dashboard),
    path('uploading/',views.upload),
    path('sendRequest/',views.uploadVideo),
]
