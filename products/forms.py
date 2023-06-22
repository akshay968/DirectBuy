from .models import Product,Variant
from django.forms.models import inlineformset_factory 
from django import forms
from .models import Variant
from products.models import ReviewRating
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'image', 'description', 'price', 'is_available', 'discount']
        labels = {
            'name': 'Product Name',
            # 'slug': 'Slug',
            # 'vendor': 'Vendor',
            'category': 'Category',
            'image': 'Product Image',
            'description': 'Product Description',
            'price': 'Price',
            'is_available': 'Is Available',
            'discount': 'Discount'
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'price': forms.NumberInput(attrs={'step': 'any'}),
            'discount': forms.NumberInput(attrs={'step': 'any'}),
        }
class VariantForm(forms.ModelForm):
    class Meta:
        model = Variant
        fields = ['variant_name','price']
        labels = {
            'variant_name': 'Variant Name',
            'price': 'Price',
            
        }        
    
VariantFormSet = inlineformset_factory(Product, Variant, form=VariantForm, extra=3)

class CartItemForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'quantity-input', 'min': 1, 'value': 1}))
    variant=forms.ModelChoiceField(queryset=Variant.objects.none(),empty_label=None)
    def __init__(self, product_id, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.product_id = product_id
          self.fields['variant'].queryset = Variant.objects.filter(product_id=self.product_id)
        
    def clean_variant(self):
        variant = self.cleaned_data['variant']
        if variant.product_id != self.product_id:
            raise forms.ValidationError("Invalid variant selected.")
        return variant
    


class ReviewForm(forms.ModelForm):
    class Meta:
        model:ReviewRating
        fields=['subject','review','rating']
