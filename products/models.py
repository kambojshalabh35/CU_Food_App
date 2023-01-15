from django.db import models
from adminAndSellers.models import Seller
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    seller_linked_user = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=55)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    added_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True) 
    noofsales = models.DecimalField(max_digits=8, decimal_places=0, default=0)

    def __str__(self):
        return str(self.title)+" - "+str(self.seller.shop_name)

class Order(models.Model):
    orderNumber = models.AutoField(primary_key=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=55)
    title = models.CharField(max_length=50)
    quantity = models.IntegerField()
    contactNumber = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    order_type = models.BooleanField()
    image = models.TextField(blank=True, null=True)
    block = models.TextField(blank=True, null=True)
    landmark = models.TextField(blank=True, null=True)
    delivery_status = models.TextField(blank=True, null=True)
    order_time = models.DateTimeField(auto_now_add=True)
