from django.shortcuts import render
from django.views import View
from .forms import CartAddForm
# Create your views here.
class CartView(View):
    def get (self,request):
        form = CartAddForm
        return render (request, 'orders/cart.html', {'form':form})
    
    