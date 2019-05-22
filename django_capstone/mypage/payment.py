import json, requests, datetime, uuid
from django.urls import reverse
from .models import Order
from django.http import *
from django.shortcuts import render, redirect, get_object_or_404
from main.models import User
from django.contrib.auth.decorators import login_required

tossapi_url = "https://pay.toss.im/api/v1/"

available_amount = [
    9900,
    19900,
    49900
]


@login_required(login_url='/social/')
def payment_request(request, amount):

    if amount not in available_amount:
        return render(request, 'alert.html', {'msg': "Do not change amount of payment."})
    owner = request.user.username

    url = tossapi_url + "payments"
    orderNo = str(uuid.uuid4())
    amount = str(amount)
    params = {
        "orderNo": orderNo,
        "amount": amount,
        "amountTaxFree": 0,
        "productDesc":"테스트 결제",
        "apiKey": "sk_test_apikey1234567890",
        "resultCallback": "https://myshop.com/toss/result.php",
        "retUrl": "https://mayak.kr"
        # "retUrl": "http://localhost:8000"
        + reverse('payment_success', kwargs={'amount': amount, 'owner':owner}), #결제 유효성 확인
        "cashRecipt": False
    }

    r = requests.post(url, data=params)
    data = json.loads(r.text)
    
    if data['code'] == 0:
        user_instance = User.objects.filter(user_name=owner).get()
        #결제가 제대로 되어있는지 확인하기 위해 payToken 변수를 저장해야 함.
        Order.objects.create(payToken=data['payToken'],orderNo=orderNo, owner = user_instance)
        #data['checkoutPage']에 리다이랙트해야할 url이 저장됨.
        return HttpResponseRedirect(data['checkoutPage'])
    else:
        return redirect('payment_fail')

#결제를 제대로 실행됬는지 확인하기 위해 필요.
@login_required(login_url='/social/')
def payment_success(request, amount, owner):
    # orderNo로 payToken가져와서 check
    orderNo = request.GET['orderNo']
    payToken = get_object_or_404(Order, orderNo=orderNo).payToken
    # 결재가 제대로 시도 된것은 결제 요청을 보내기 전 payToken과
    # orderNo로 받은 payToken이 같은지를 이용해서 check
    if "PAY_APPROVED" != payment_check(payToken):
        return redirect('payment_fail')

    # Update user DB
    user_instance = User.objects.filter(user_name=owner).get()
    user_instance.membership_remaining += 30
    user_instance.total_pay += amount
    user_instance.save()

    return render(request, 'payment_success.html')

@login_required(login_url='/social/')
def payment_fail(request):
    #진우형 payment_fail.html 대신에 형 fail html 파일 만든다음 경로 설정해주세요.
    return render(request, 'payment_fail.html')
    
##### request-handling function end #######
###### non-request-handling function ######
def payment_check(token):
    url = tossapi_url + "status"
    params = {
        "payToken": token,
        "apiKey": "sk_test_apikey1234567890",
    }
    r = requests.post(url, data=params)
    data = json.loads(r.text)
    if data['code'] == 0:
        return data['payStatus']
    else:
        return None

