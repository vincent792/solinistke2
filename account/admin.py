from django.contrib import admin

# Register your models here.
from  .models import Account,Activation,Mpesa
admin.site.register(Account)
admin.site.register(Activation)
admin.site.register(Mpesa)