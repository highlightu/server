from django.urls import path
from django.conf.urls import include  # url뿐 아니라 include를 import해야 합니다.
from . import views
from upload.views import *  # 3rd app : upload

urlpatterns = [
    path('', views.dashboard),
    # history
    path('history/', views.history, name='history'),
    # upload
    path('upload/', include('upload.urls'), name='upload'),
]
