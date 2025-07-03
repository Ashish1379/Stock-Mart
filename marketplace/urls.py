from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns =[
  path('' , views.home ,name = 'home') ,
  path('market/' , views.showStocks , name = 'market') ,
  path('data/', views.getData , name = 'data') ,
  path('login/', views.loginView , name='login'),
  path('logout/', views.logoutView , name='logout') ,
  path('register/', views.registerView , name = 'register') ,
  path('market/buy/<str:id>/' , views.buy , name = 'buyStock') ,
  path('market/sell/<str:id>/' , views.sell , name = 'sellStock')
 ]

urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)