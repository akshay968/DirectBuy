from django.db import models
from django.urls import reverse
# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='category/images/', blank=True)

    # class Meta:
    #     verbose_name = 'category'
    #     verbose_name_plural = 'categories'
    
    # def get_url(self):
    #     return reverse('products_by_category', args=[self.slug])

    # def __str__(self):
    #     return self.category_name
class Product(models.Model):
    name =models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    vendor=models.ForeignKey('Person', null=True, blank=True,related_name='ownwer',on_delete=models.CASCADE)
    category=models.ForeignKey('Category')
    description=models.TextField(max_length=2000)
    variant=models.ManyToManyField('Type', blank=True)
    price=models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    discount=models.DecimalField(max_digits=5,decimal_places=2,default=0)
    # virtualproduct=models.BooleanField(default=0)
    # productfile=models.FileField()

