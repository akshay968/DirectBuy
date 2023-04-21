from django.contrib import admin
from .models import Product,Category,Variant
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'slug']
    prepopulated_fields = {'slug': ('category_name',)}
    
class ProductAdmin(admin.ModelAdmin):
    list_display=['name','slug']
    prepopulated_fields={'slug':('name',)}
class VariantAdmin(admin.ModelAdmin):
    list_display=['variant_name']
    # prepopulated_fields={'slug':('name',)}
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Variant, VariantAdmin)

