from .models import *
from django.contrib import admin
# Register your models here.

# admin.site.register(UserInfo)
@admin.register(UserStock)
class UserStockAdmin(admin.ModelAdmin):
        ordering = ('user' , )
        list_display = ('user', 'stock','purchase_quantity', 'purchase_price',  'purchaseDate')
         

@admin.register(Stocks)
class StockAdmin(admin.ModelAdmin) : 
    list_display = ('ticker' ,  'name' ,  'curr_price')

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin) : 
    list_display = ('user' ,  'phone_number' ,  'address' , 'pancard_number' ,'user_image' , 'pancard_image')