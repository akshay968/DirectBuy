from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.views import View
from .models import Product,Variant
from .models import Category,Account
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from .forms import ProductForm,VariantForm
from django.urls import reverse
from django.forms import modelformset_factory
from cart.views import add_cart
from .forms import CartItemForm
# Create your views here.

def startpage(request):
    return render(request,'products/startpage.html')

def index(request,category_slug=None):
    # print(request.user.id)
    allproducts=None
    count=0
    if(category_slug==None):
        allproducts=Product.objects.all()
        count=allproducts.count()
    else:
        category_model=get_object_or_404(Category,slug=category_slug)
        allproducts=Product.objects.filter(category=category_model)
        count=allproducts.count()
            
    # print(allproducts[0])
    return render(request,'products/index.html',{ 'products':allproducts ,'products_count':count} )
@login_required(login_url='login')
def add_product(request):
    # Create an empty formset for the variants
    VariantFormSet = modelformset_factory(Variant, form=VariantForm, extra=3,can_delete=True)

    if request.method == 'POST':
        # Create a form instance and a formset instance with the POST data
        product_form = ProductForm(request.POST, request.FILES)
        variantformset = VariantFormSet(request.POST)
           
        if product_form.is_valid() and variantformset.is_valid():
            # Save the product instance
            product = product_form.save(commit=False)
            product.slug = slugify(product.name)
            product.vendor = request.user
            product.save()

            # Save the variant instances
            for variant_form in variantformset:
                variant = variant_form.save(commit=False)
                variant.product = product
                variant.save()

            return HttpResponse('Product added successfully!')

        else:
        # Create an empty form instance and formset instance
             context={
             'product_form':product_form,
             'variant_form':variantformset
             }  
             return render(request,'products/add_product.html',context)  
    else:
        
        product_form=ProductForm()
        variant_form=VariantFormSet(queryset=Variant.objects.none())

        context={
            'product_form':product_form,
            'variant_form':variant_form
        }  
        return render(request,'products/add_product.html',context)  


    
def edit_product(request,pk):
    VariantFormSet = modelformset_factory(Variant, form=VariantForm, extra=3,can_delete=True)

    product=get_object_or_404(Product,pk=pk)   
    print(request.method)
    if request.method=='POST':
         
        product_form=ProductForm(request.POST,instance=product)
        variant_formset=VariantFormSet(request.POST,queryset=Variant.objects.filter(product=product))
        if product_form.is_valid() and variant_formset.is_valid():
            product=product_form.save(commit=False)
            product.slug=slugify(product.name)
            product.save()
            for variant_form in variant_formset:
               if variant_form.is_valid():
                  
                   variant = variant_form.save(commit=False)
                   variant.product = product
                   variant.save()
                   if variant.variant_name=="":
                       Variant.delete(variant)

            for deleted_form in variant_formset.deleted_forms:
                if deleted_form.instance.pk:
                    deleted_form.instance.delete()
          
    
            return HttpResponse("edited") 
        else:
            revere_url=reverse('edit_product',args=[pk])
            context={
            'product_form':product_form,
            'variant_form':variant_formset,
            'reverse_url':revere_url
        }
        return render(request,'products/edit_product.html',context)  

    else:
        product_form=ProductForm(instance=product)
        print(product_form)
        variant_formset=VariantFormSet(queryset=Variant.objects.filter(product=product))
        revere_url=reverse('edit_product',args=[pk])
        context={
            'product_form':product_form,
            'variant_form':variant_formset,
            'reverse_url':revere_url
        }
        return render(request,'products/edit_product.html',context)   
    
def sell_page(request):
    products=Product.objects.filter(vendor=request.user)
    context={
        'products':products,
     }
    return render(request,'products/sell.html',context)

def product_detail(request,product_slug):
     product=Product.objects.get(slug=product_slug)
     if request.method=='POST':
        cartitem_form=CartItemForm(product.id,request.POST)
        if cartitem_form.is_valid():
            variant=cartitem_form.clean_variant()
            quantity=cartitem_form.cleaned_data.get('quantity')
            return add_cart(request,product.pk,variant.pk,quantity)
          
        else:
             context={
            'product':product,
            'cartitem_form':cartitem_form,
        }
    
        return render (request,'products/product_detail.html',context)       

     else:   
        cartitem_form=CartItemForm(product.id)
        context={
            'product':product,
            'cartitem_form':cartitem_form,
        }
    
     return render (request,'products/product_detail.html',context)