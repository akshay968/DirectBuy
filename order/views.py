from django.shortcuts import render,HttpResponse
from django.urls import reverse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from cart.forms import CheckoutForm
# Create your views here.

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
@login_required(login_url='login')
def placeorder(request):
  if request.method=='POST':
    current_user=request.user
    cart_items=CartItem.objects.filter(user=current_user)
    total=0
    order=CheckoutForm(request.POST)
    if order.is_valid():
        order.save(commit=False)
        order.user=current_user
        order.save()
    for cart_item in cart_items:
       total+=cart_item.quantity*cart_item.price
       quantity=cart_item.quantity
       print(cart_item.quantity)
       print(cart_item.price)
    grand_total=total+(2*total)/100

    amount=(int)(grand_total*100+10000) #for razorpay 
    print(amount)
    currency = 'INR'
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture=1))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = reverse('paymenthandler')
 
    # we need to pass these details to frontend.
    context = {
        'order':order

    }
    # print(payment_id)
    print(razorpay_order)
    # print(signature)
    context['razorpay_order']=razorpay_order
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['rurl']=reverse('paymenthandler')
    context['amount']=amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    return render(request, 'order/place_order.html', context=context) 
  else:
      pass
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
   
    # only accept POST request.
    if request.method == "POST":
        try:  
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
             # Rs. 200
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            print(payment_id)
            print(razorpay_order_id)
            print(request.POST)
            # print(request.POST['amount'])
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            print(result)
           
            # amount=(int) (request.POST.get('amount',''))
            # amount=10000
            # print(amount)
            print(result)
            if result is not None:
                
                # print(amount)
                try:
                    
                    # capture the payemt
                    # razorpay_client.payment.capture(payment_id)
                    
                    # render success page on successful caputre of payment
                    return HttpResponse("paymentsuccess")
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
