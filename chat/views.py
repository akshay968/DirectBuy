from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,reverse,redirect
from accounts.models import  Account
from django.db.models import  Q
# import channels
# Create your views here.
from chat.models import Thread
from products.models import  Product

@login_required
def messages_page(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    context = {
        'Threads': threads,
    }
    return render(request, 'chat/messages.html',context)


def contact_vendor(request,vendor_id):
    product_id=(request.POST.get('product_id'))
    print(product_id)
    # print(request.POST['product_id'])
    product_is=Product.objects.get(id=product_id)
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    first_person = request.user
    second_person = Account.objects.get(id=vendor_id)
    thread_qset = Thread.objects.filter(
        Q(first_person=first_person, second_person=second_person) | Q(first_person=second_person,
                                                                      second_person=first_person))
    thread1 = None
    if thread_qset.exists():
        thread1 = thread_qset[0]
    else:
        new_thread = Thread(first_person=first_person, second_person=second_person)
        new_thread.save()
        thread1 = new_thread
    query1= "query regarding"+" "+product_is.name
    context = {
        'Threads': threads,
        'thread1': thread1,
        'query1':query1
    }
    return render(request, 'chat/messages.html', context)


