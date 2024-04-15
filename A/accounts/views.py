from django.shortcuts import render , redirect
from django.views import View
from .forms import UserRegistrationForm , VerifyCodeForm
import random
from utils import send_otp_code
from .models import OtpCode , User
from django.contrib import messages


class UserRegisterView(View):

    form_class= UserRegistrationForm
    template_name ='accounts/register.html'

    def get(self,request):
        form = self.form_class
        return render(request,self.template_name , {'form':form} )
    
    def post (self,request):
        form=self.form_class(request.POST)

        if form.is_valid():
            random_code= random.randint(1000,9999)    #this random number should have a period for choosing random number
            send_otp_code(form.cleaned_data['phone'] , random_code)   #here our sms will send
            #now we goiong to our model and saving the phone that we just get from user and the random code we just created.
            OtpCode.objects.create(phone_number=form.cleaned_data['phone'] , code=random_code)
            #now we should've save other details of user in sessions. like email and fullname . 
            #in chizi ke tooye bracket minevisim ye kilide ke khodemon mizarim
            request.session['user_registration_info'] = {
				'phone_number': form.cleaned_data['phone'],
				'email': form.cleaned_data['email'],
				'full_name': form.cleaned_data['full_name'],
				'password': form.cleaned_data['password'],
            }
            messages.success(request, 'we just send you a code', 'success')
            return redirect ('accounts:verify_code')
        return render (request,self.template_name, {'form':form})
    

#hala mikhaym check konim bebinim on addadi ke user vared mikone tooye on form e tak fieldi e ke mibine, ba on code e randomi ke ma sakhtimo tooye data base akhirash karde bodim yekie ya na age yeki bood pas useremon verify mishe va ye usere jadid sakhte mishe age yeki nabood, bayad dobare redirect beshe be on form dobare
#ba estefade az session ha ma etelaate user ro az formi ke tooye url ghabli bood darim. miaym ba phone number ke too session hast on filed e marboote ro too database peyda mikonim ke betoonim code e yebar masrafe marboote ro peyda konim ke on cod  ro ba code i ke aalan karbar vared karde moghayese konim
class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm
    def get (self,request):
        form= self.form_class
        return render (request, 'accounts/verify.html' , {'form':form})

    def post (self,request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)

        if form.is_valid():
            cd= form.cleaned_data
            if cd['code']==code_instance.code:
                User.objects.create_user(user_session['phone_number'], user_session['email'] ,
                                         user_session['full_name'], user_session['password'])
                code_instance.delete()
                messages.success(request, 'you are verified' , 'success')
                return redirect('home:home')
            else:
                messages.error(request,'your code is incorrct', 'danger')
                return redirect('accounts:verify_code')
        return redirect ('home:home')    
    
    







