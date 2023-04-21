from django.shortcuts import render,redirect
from django.views import View
from .forms import RegistrationForm
from .models import Account
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages,auth
from django.http import HttpResponseRedirect,HttpResponse

# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from cart.models import Cart,CartItem
from cart.views import _cart_id
# Create your views here.

def login(request):
    return render(request,'accounts/login.html')
class signup(View):
   def get(self,request):
     Rform=RegistrationForm()
     reverse('signup')
     return render(request,'accounts/signup.html',{'form':Rform,'re_url':reverse('signup')})
   def post(self,request):
      
      submitted_Rform=RegistrationForm(request.POST)
      if submitted_Rform.is_valid():
            
            first_name = submitted_Rform.cleaned_data['first_name']
            last_name = submitted_Rform.cleaned_data['last_name']
            email = submitted_Rform.cleaned_data['email']
            phone_number = submitted_Rform.cleaned_data['phone_number']
            password = submitted_Rform.cleaned_data['password']
            # user = submitted_Rform.save(commit=False)
            username=email.split('@')[0]
            # user.phone_number=phone_number
            # user.set_password(submitted_Rform.cleaned_data['password'])
            # user.save()
           
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            
            # User Activation
            
            current_site = get_current_site(request)
            mail_subject = 'Please Activate Your Account To Login!'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            print("saved")
            to_email = email
            print("email")
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            # messages.success(request, 'Get ready! verify your email & get started')
            return HttpResponseRedirect('/accounts/login/?command=verification&email='+email)
      
      context = {
           'form': submitted_Rform,
        }
      return render(request, 'accounts/signup.html', context=context)
   


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congo! Your account is Activated')
       
        return HttpResponseRedirect( reverse('login'))
    else:
        messages.error(request, 'Invalid Activation Link')
        return HttpResponseRedirect('accounts/register')


class login(View):
    def get(self,request):
        re_url= reverse('login')
        return render(request,'accounts/login.html',{ "re_url" :re_url } ) 
    
    def post(self,request):
        email=request.POST['email']
        password=request.POST['password']
        user =auth.authenticate(request,email=email,password=password)
        if user is  None:
            print("invalid")
            messages.error(request, 'Invalid Login Credentials')
            urll=reverse('account_login')
            return HttpResponseRedirect(urll)
        else :
            #before login we need add the cartitem in the session 
            #we use session key as identifier before login but 
            #after login filter through user
          try:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
            if is_cart_item_exists:
                    cart_items = CartItem.objects.filter(cart=cart)
            
            for cart_item in cart_items:
                try:
                    user_cart_item=CartItem.objects.get(user=user,product=cart_item.product,variant=cart_item.variant)
                    user_cart_item.quantity+=cart_item.quantity
                    user_cart_item.save()
                    cart_item.delete()
                except:
                    cart_item.user=user
                    cart_item.save()    
          except:
            pass
            auth.login(request,user)
            return redirect(reverse('index'))
        
@login_required
def logout(request):
    auth.logout(request)
    return  redirect(reverse('index'))
