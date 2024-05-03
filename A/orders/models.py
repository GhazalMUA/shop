from django.db import models
from django.contrib.auth import get_user_model
from home.models import Product
from django.core.validators import MaxValueValidator,MinValueValidator
# Create your models here.

class Order(models.Model):
    user=models.ForeignKey(get_user_model() , on_delete=models.CASCADE , related_name= 'orders')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    paid=models.BooleanField(default=False)
    discount=models.IntegerField(blank=True , null= True, default=None)
    
    class Meta:
        ordering=('paid', '-updated')
        
    def __str__(self):
        return f'order {self.id} - {self.paid}'
        
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())         #self.items.all() yani az tarighe related name e field e order tooye kelase orderitem, hameye order haro begir toosh halghe bezan va inke tak take orderha ye get_cost i daran ke tedad dar gheymateshono moshakhas mikone natijeye inaro baham jam kon mishe total price e sabad kharid et
        
        
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product , on_delete=models.CASCADE, related_name='order_items')
    price=models.IntegerField()
    quantity=models.IntegerField(default=1)
    
    
    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity
    
    
    
    
    class Coupan(models.Model):
        discount=models.IntegerField(validators=[MinValueValidator(0) , MaxValueValidator(90)])
        valid_from=models.DateTimeField
        valid_to=models.DateTimeField
        code=models.CharField(max_length=20, unique=True)
        active=models.BooleanField(default=False)