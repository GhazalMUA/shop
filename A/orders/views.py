from django.shortcuts import render , get_object_or_404 , redirect
from django.views import View
from .forms import CartAddForm , CoupanApplyForm
from .cart import Cart
from home.models import Product
from .models import Order , OrderItem , Coupan
from django.contrib.auth.mixins import LoginRequiredMixin , PermissionRequiredMixin
from django.conf import settings
import requests
import json
from django.http import JsonResponse
import datetime
from django.contrib import messages








# Create your views here.
class CartView(View):
    def get (self,request):
        cart=Cart(request)
        return render (request, 'orders/cart.html', {'cart':cart})
    
    
class CartAddView(View):
    def post(self,request, product_id):            #after i created cart.py i can write this view. id and quantity will come to me by form(the form that I linked it to my urls. the url that connected to this view.)
        cart= Cart(request)
        form=CartAddForm(request.POST)
        product=get_object_or_404(Product,id=product_id)
        if form.is_valid():
            quantity=form.cleaned_data['quantity']
            cart.add(product,quantity)
        return redirect('orders:cart')
    

class CartRemoveView(PermissionRequiredMixin,View):           #PermissionRequiredMixin in male vaghtie k mikhay baresi koni karbar on dastresi ro dare ya na. noe dastresi ro ham permission_required moshakhas mikone. age yedone bashe mesle mn minevisim . age chandta bashe tooye list ya tuple minevisimesh
	permission_required = 'orders.add_order'
 
	def get(self, request, product_id):
		cart = Cart(request)
		product = get_object_or_404(Product, id=product_id)
		cart.remove(product)
		return redirect('orders:cart')

class OrderDetailView(LoginRequiredMixin,View):
    def get(self,request, order_id):
        order=get_object_or_404(Order, id=order_id)
        form= CoupanApplyForm
        return render(request, 'orders/order.html', {'order':order , 'form':form} )
        
    
class OrderCreateView(LoginRequiredMixin,View):
    def get(self,request):
        cart=Cart(request)
        order=Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(order=order ,product=item['product'], price=item['price'], quantity=item['quantity'] )
        cart.clear()
        return redirect('orders:order_detail' , order.id)
    
    
    
################################## zarinpal ######################################    
    
MERCHANT = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
CallbackURL = 'http://127.0.0.1:8000/orders/verify/'

class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        request.session['order_pay'] = {
            'order_id': order.id
                                        }

        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.get_total_cost(),
            "Description": description,
            "Phone": request.user.phone_number,  # Optional
            "CallbackURL": CallbackURL,
        }
        headers = {'content-type': 'application/json'}
        try:
            response = requests.post(ZP_API_REQUEST, json=data, headers=headers, timeout=10)
            if response.status_code == 200:
                response_data = response.json()
                if response_data['Status'] == 100:
                    authority_url = ZP_API_STARTPAY.format(authority=response_data['Authority'])
                    return JsonResponse({'status': True, 'url': authority_url, 'authority': response_data['Authority']})
                else:
                    return JsonResponse({'status': False, 'code': str(response_data['Status'])})
            return JsonResponse({'status': False, 'code': str(response.status_code)})
        except requests.exceptions.Timeout:
            return JsonResponse({'status': False, 'code': 'timeout'})
        except requests.exceptions.ConnectionError:
            return JsonResponse({'status': False, 'code': 'connection error'})
    




class OrderVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        order_id = request.session['order_pay']['order_id']
        if not order_id:
            return JsonResponse({'status': False, 'code': 'no order found'})

        order = Order.objects.get(id=int(order_id))
        authority = request.GET.get('Authority')  

        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.get_total_cost(),  # Use the correct method name for total cost
            "Authority": authority,
        }
        headers = {'content-type': 'application/json'}
        response = requests.post(ZP_API_VERIFY, json=data, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            if response_data['Status'] == 100:
                order.paid = True
                order.save()
                return JsonResponse({'status': True, 'RefID': response_data['RefID']})
            else:
                return JsonResponse({'status': False, 'code': str(response_data['Status'])})
        return JsonResponse({'status': False, 'code': str(response.status_code)})


 
 
class ApplyCoupanView(LoginRequiredMixin, View):
    def post(self,request,order_id):
        now=datetime.datetime.now()
        form= CoupanApplyForm(request.POST)
        if form.is_valid():  
            applied_code=form.cleaned_data['code']
            try:
                coupan=Coupan.objects.get(valid_from__lte=now , valid_to__gte=now ,code__exact=applied_code, active=True)
            except Coupan.DoesNotExist:
                messages.error(request, 'this code does not exist' , 'danger')
                return redirect ('orders:order_detail' , order_id)
            
            order=Order.objects.get(id=order_id)
            order.discount = coupan.discount
            order.save()
        return redirect ('orders:order_detail' , order_id)