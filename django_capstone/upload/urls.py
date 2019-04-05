from django.urls import path
from django.conf.urls import include  # url뿐 아니라 include를 import해야 합니다.
from . import views

urlpatterns = [
    path('', views.upload),

    # loading
    path('loading/', views.loading, name='loading'),
]
