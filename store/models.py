from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore

# Create your models here.

class Category(models.Model):

    name = models.CharField(max_length=100)
    Image = models.FileField(upload_to="img/",default="static/img/place_holder_default.jpg")

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    Image = models.FileField(upload_to="img/",default="static/img/place_holder_default.jpg")
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=225,null=True,blank=True)
    phone = models.CharField(max_length=15,null=True,blank=True)

    
    def __str__(self):
        return self.user.username

class CartItem(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    def get_total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    superuser = models.ForeignKey(User,related_name='superuser_orders',on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='user_orders',on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(CartItem)
    shipping_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=50)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"