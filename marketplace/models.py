from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserInfo(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length = 500)
    pancard_number = models.CharField(max_length=30)
    user_image = models.ImageField()
    pancard_image=  models.ImageField()
    
# four steps to handle images:
# 1. use ImageField() for storing images
# 2. make sure pillow is installed
# 3. media url in settings
# 4.static url in urls.py


class Stocks(models.Model):
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length= 300)
    description = models.CharField(max_length= 5000)
    curr_price = models.FloatField()

    def __str__(self):
        return self.name

class UserStock(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    stock  = models.ForeignKey(Stocks ,  on_delete= models.CASCADE)
    purchase_price  =  models.FloatField()
    purchase_quantity =  models.IntegerField()
    purchaseDate =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  self.stock.name + " " + str(self.user.username)