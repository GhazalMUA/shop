#i dont want my views to be busy and messy so i devided cart codes which insclude session codes, from other part here.ValueError
from home.models import Product
CART_SESSION_ID = 'cart'

class Cart:
    def __init__(self,request):
        self.session= request.session
        cart = self.session.get(CART_SESSION_ID)   #this is for the time that user was in our website befor and has a previous cart. // when we use get() method, it will check if any thing exists in the query or now. remember that get() method only returns one item. if there wasnt any item in the cart it will returns None.
        if not cart:              #this is about when it returns None. it means that:this is the first time that user is on my website. and you should create cart (session) for this user.
           cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart
    
    def __iter__(self):
        product_ids= self.cart.keys()
        products=Product.objects.filter(id__in=product_ids)                        #search in products and give me the one which its id is (product_ids). product_ids is a list so for checking id in this list you should usr __in to iterate
        cart = self.cart.copy()                   #we want to amke changes in the cart. for example adding some options(besorate key and value) so we should have a copy of main cart and then make changes.
        for product in products:
            cart[str(product.id)]['product'] = product    #here i the dictionary of the specific profile with key:product.id , we add a new opthion (key) named 'product within a value product.name
        for item in cart.values(): 
            item['total_price'] = float(item['price']) * item['quantity']
            yield item
     
    def __len__(self):                               #in function har natijei ro ke return kone mishe length e in class madar. yani alan masalan kelasmon Cart hast va yejai mikhaym be len esh dastresi dashte b ashim vali chon in class cart ghabele shomaresh nistesh, bayad vasash ye method __len__() taain konim ke tooye on moshakhas konim k jahaye dg vase len() che meghdari bargardonde beshe        
        return sum(item['quantity'] for item in self.cart.values())
       
    def add(self,product,quantity):
        product_id = str(product.id)
        if product_id not in self.cart:                                             #if that product was not in the card, so I will create a session and if it was exists i will add that product to that card
            self.cart[product_id] ={'quantity': 0 , 'price':str(product.price)}     #all data, will be stored by string in session. so when you want to add something manually in sessions, you should have make that element string first then save the data.
        self.cart[product_id]['quantity'] += quantity                               #if that product exists in cart befor, add the quantity that user added o the quantity you had befor in user's session.
        self.save()                                                                 #because we add the product manually, we should save the session. we want to be away of repeatition so we careate a method (save) in this class which saves the changes. we do this because we want to use it many time we can now save things in this class just with self.save     self is a connection between differenet methods of one class.
    
    def save(self):
        self.session.modified = True
        
    def remove(self,product):
        product_id=str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()      
            
        
    def get_total_price(self):
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())
        
    
    
    