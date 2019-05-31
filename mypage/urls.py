from django.urls import path
from . import views
from . import payment

urlpatterns = [
    path('archive/', views.archive, name='archive'),
    path('payment/', views.payment, name='payment'),

    # payment request
    path('payment/request/<int:amount>/', payment.payment_request, name='request'),
    path('payment_success/<int:amount>/<str:owner>/', payment.payment_success, name='payment_success'),
    path('payment_fail/', payment.payment_fail, name='payment_fail'),
    path('withdraw/', views.withdraw, name='withdraw'),
]
