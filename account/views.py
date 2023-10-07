from django.shortcuts import render,redirect,get_object_or_404
from  django.contrib import messages,  auth
from  account.models import Account,Activation,Mpesa
from django.contrib.auth.models import User
from django.urls import reverse
# Create your views here.
def register(request):
    if  request.method=='POST':
        uname=  request.POST['uname']
        email=  request.POST['email']
        phone=  request.POST['phone']
        pass1=  request.POST['pass1']
        user=User.objects.create_user(username=uname, password=pass1, email=email)
        user.save()
        user1=Account(user=user,username=uname, phone=phone, email=email)
        user1.save()
        print('user saved to  db')
        return redirect('login')    
        

    return render(request,  'account/register.html')

def login(request):
    if  request.method=='POST':
        uname=  request.POST['uname']
        pass1=  request.POST['pass1']
        user=auth.authenticate(username=uname, password=pass1)
        if  user is not  None:
            auth.login(request, user)
            print('user saved loged in')
            return redirect('/') 
        else:
            print('invalid')

        
    return render(request,  'account/login.html')


def logout(request):
    auth.logout(request)
    print('logged off')
    return redirect('login')    


#activation



def activate(request):
   
    return render(request, 'account/activate.html')

def activate1(request):
    context={}
    uname=request.user.account.username
    phone=request.user.account.phone

    if request.method == 'POST':
        uname=uname
        phone=phone
        code=request.POST['code']

        save_to_db=Activation(username=uname,phone=phone, transaction_code=code)
        save_to_db.save()
        # Use reverse() to build the URL with the required parameter
        activate_account_url = reverse('activate_account', kwargs={'mpesa_code': code})
        return redirect(activate_account_url)
    context['uname']=uname
    context['phone']=phone
    return render(request, 'account/activate1.html',context)

def activate_account(request, mpesa_code):
    uname=request.user.username
    # Find the corresponding Activation object
    activations = Activation.objects.filter(username=uname,transaction_code=mpesa_code)
    activation=activations.first()
    print(activation)
    
    # Find the corresponding Mpesa object
    mpesa = Mpesa.objects.filter(phone=activation.phone, code=activation.transaction_code).first()

    if mpesa:
        # Update the Account object's is_activated field to True
        account = get_object_or_404(Account, username=activation.username)
        account.is_activated = True
        account.save()

        # You can also delete the Activation and Mpesa objects if needed
        activation.delete()
        mpesa.delete()

     

        # Redirect or render a success page
        return render(request, 'success.html', {'message': 'Account activated successfully'})

    else:
        # Handle the case when the codes do not match
        return render(request, 'error.html', {'message': 'Invalid activation code'})
    


