#go to django's documententions in view layer see overview of middleware copy paste the class sample.
#this loginmiddleware checks if user is not authenticatet, cant see any urls except home,register,login
from django.contrib import messages
from django.shortcuts import redirect

LOGIN_EXEMP_URLS =[
    '/' , 
    '/accounts/login/' ,
    '/accounts/register/' ,
    
]

class LoginMiddleware:
    def __init__(self, get_response):                      #this is static. you dont need to change it.
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if not request.user.is_authenticated and request.path not in LOGIN_EXEMP_URLS:
            messages.warning(request , 'you should login first' , 'warning')
            return redirect ('home:home')  

        response = self.get_response(request)                  #everything before this line, is run befor the view logic and everything after this line, will run after view.

   
        return response
    