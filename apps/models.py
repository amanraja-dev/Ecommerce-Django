from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
import uuid
# Create your models here.

class ADDRESS(models.Model):
    address_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    mobile = models.CharField(max_length=10)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    zipcode = models.IntegerField()
    def __str__(self):
        return self.user.first_name

class BRAND(models.Model):
    brand_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    brand_name = models.CharField(max_length=20)
    def __str__(self):
        return self.brand_name
    
class CATEGORIES(models.Model):
    categories_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    categories = models.CharField(max_length=20)
    categories_image = models.ImageField(upload_to='categories-images',default='')
    def __str__(self):
        return self.categories

class COLOUR(models.Model):
    colour_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    colour_name = models.CharField(max_length=20)
    def __str__(self):
        return self.colour_name

GENDER_CHOICE={
    ('Man','Man'),
    ('Woman','Woman'),
}
class PRODUCT(models.Model):
    product_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    product_name = models.CharField(max_length=20)
    original_price = models.FloatField()
    selling_price = models.FloatField()

    gender = models.CharField(max_length=10,choices=GENDER_CHOICE)

    categories = models.ForeignKey(CATEGORIES, on_delete=models.CASCADE)
    colour = models.ForeignKey(COLOUR, on_delete=models.CASCADE)
    brand = models.ForeignKey(BRAND, on_delete=models.CASCADE)

    product_image = models.ImageField(upload_to='products')
    product_desc = models.TextField()
    quantity = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.product_name

class FEATURED_PRODUCT(models.Model):
    product_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    product_name = models.CharField(max_length=20)
    original_price = models.FloatField()
    selling_price = models.FloatField()

    gender = models.CharField(max_length=10,choices=GENDER_CHOICE)

    categories = models.ForeignKey(CATEGORIES, on_delete=models.CASCADE)
    colour = models.ForeignKey(COLOUR, on_delete=models.CASCADE)
    brand = models.ForeignKey(BRAND, on_delete=models.CASCADE)

    product_image = models.ImageField(upload_to='products')
    product_desc = models.TextField()
    quantity = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.product_name

class CART(models.Model):
    cart_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  
    product = models.ForeignKey(PRODUCT, on_delete=models.CASCADE)  
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return self.user.first_name

STATUS_CHOICE={
    ('Order Confirmed','Order Confirmed'),
    ('Shipped','Shipped'),
    ('Out For Delivery','Out For Delivery'),
    ('Delivered','Delivered'),
    ('Cancle','Cancle')
}
class ORDER(models.Model):
    order_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) 
    address = models.ForeignKey(ADDRESS, on_delete=models.CASCADE) 
    product = models.ForeignKey(PRODUCT, on_delete=models.CASCADE)  
    quantity = models.PositiveIntegerField(default=1)
    orderdate  = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICE, default='pending')
    def __str__(self):
        return self.user.first_name

class WISHLIST(models.Model):
    wishlist_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(PRODUCT, on_delete=models.CASCADE)  
    def __str__(self):
        return self.user.first_name