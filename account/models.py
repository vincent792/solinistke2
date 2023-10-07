from django.db import models

# Create your models here.
from  django.contrib.auth.models import User
# Create your models here.
class Account(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    username=models.CharField(max_length=40, unique=True)
    phone=models.CharField(max_length=255, unique=True)
    email=models.EmailField(max_length=255, unique=True)
    is_activated=models.BooleanField(default=False)
    activation_code=models.CharField(max_length=100, blank=True, null=True)
    phone=models.CharField(max_length=13, null=True, blank=True)

    def __str__(self) -> str:
        return self.username
    

class Activation(models.Model):
    transaction_code=models.CharField(max_length=255)
    phone=models.CharField(max_length=13)
    username=models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.username
    
class Mpesa(models.Model):
    code=models.CharField(max_length=100)
    phone=models.CharField(max_length=13)

    def __str__(self) -> str:
        return self.code