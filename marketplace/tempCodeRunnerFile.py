from django.contrib import admin
# Register your models here.

# admin.site.register(UserInfo)
@admin.register(UserStock)
class UserStockAdmin(admin.ModelAdmin):
    # list_display = ('user')
    # for stocks in 'stock':
    print('user' , 'stock')