from django.db import models
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self,phone_number,email,full_name,password):
        if not phone_number:
            raise ValueError ('user must have a valid phone number')
        if not email:
            raise ValueError ('user must have a valid email')
        if not full_name:
            raise ValueError ('user must have a valid full name')
        
        user = self.model(phone_number=phone_number, email=self.normalize_email(email), full_name=full_name )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,phone_number,email,full_name,password):
        user= self.create_user(phone_number,email,full_name,password)
        user.is_admin=True
        user.save()
        return user
        
     