from django.shortcuts import render
from products.models import Product,Variant
from accounts.models import Account
from django.conf import settings
from .models import Cart,CartItem
from django.shortcuts import redirect
from .forms import CheckoutForm
# Create your views here.
def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def index(request):
    variant=None
    cart=None
    cart_item=None
    current_user=request.user
    tax = 0
    grand_total = 0
    total=0
    context=None
    quantity=0
    if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
            context = {
            'cart_items': cart_items,
            }
            
    else:
            
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request)) 
                cart_items = CartItem.objects.filter(cart=cart)
              
            except:
                pass  
    for cartitem in cart_items:
       total+=cartitem.quantity*cartitem.price
       quantity=cartitem.quantity
       grand_total+=(2*total)/100
       
    context = {
                'total': total,
                 'quantity':quantity,
                'cart_items': cart_items,
                'tax'         : tax,
                'grand_total': grand_total,
             }          
    return render(request, 'cart/cart.html', context)

def add_cart(request,product_id,variant_id,quantity):
   
    product=Product.objects.get(pk=product_id)
    variant=None
    cart=None
    cart_item=None
    current_user=request.user
    if variant_id is None:
        variant=None
    else:
        variant=Variant.objects.get(pk=variant_id)
        print(variant.price)
    if current_user.is_authenticated:
     try:
        cart_item= CartItem.objects.get(user=current_user,product=product,variant=variant) 
        # cart_item.save(commit=False)
        
        cart_item.quantity+=quantity 
        cart_item.save()
     except:
        cart_item=CartItem.objects.create(user=current_user,product=product,variant=variant,price=variant.price,quantity=quantity)
       

        cart_item.save()
    else:
        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))
        except:
            cart=Cart.objects.create(
            cart_id=_cart_id(request)
            )    
            cart.save()   
        try:
            cart_item= CartItem.objects.get(cart=cart,product=product,variant=variant) 
            cart_item.quantity+=quantity 
            cart_item.price=variant.price
            cart_item.save()
        except:
            cart_item=CartItem.objects.create(cart=cart,product=product,variant=variant,quantity=quantity)
            cart_item.save()
   
    return redirect('cart')  

def checkout(request):
      addform=CheckoutForm()
      context={
          'check_outform':addform,
      }
      return render(request,'cart/checkout.html',context)
