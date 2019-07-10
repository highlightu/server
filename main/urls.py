from django.urls import path
from django.conf.urls import include  # url뿐 아니라 include를 import해야 합니다.
from . import views
from dashboard.views import *  # 2nd app : dashboard


SOCIAL_AUTH_URL_NAMESPACE = 'social'

LOGIN_REDIRECT_URL = '/'

urlpatterns = [
    # homepage
    path('', views.goHome),
    path('home/', views.index, name='home'),

    # google login
    path('social/', views.social_login, name='login_social'),

    # authentication with google
    path('oauth/', include('social_django.urls', namespace='social')),

    # logout
    path('logout/', views.logout, name='logout'),

    # dashboard
    path('mypage/dashboard/', include('dashboard.urls'), name='dashboard'),

]
