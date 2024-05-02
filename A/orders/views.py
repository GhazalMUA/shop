from django.shortcuts import render , get_object_or_404 , redirect
from django.views import View
from .forms import CartAddForm
from .cart import Cart
from home.models import Product
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
    

class CartRemoveView(View):
	def get(self, request, product_id):
		cart = Cart(request)
		product = get_object_or_404(Product, id=product_id)
		cart.remove(product)
		return redirect('orders:cart')