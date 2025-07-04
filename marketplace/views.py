
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
import requests
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib  import messages
# Create your views here.

@login_required
def home(request):
    user = request.user
    user_stocks = UserStock.objects.select_related('stock').filter(user = user)

    total_value = 0
    invested = 0

    for item in user_stocks:
        stock_value = item.purchase_quantity * item.stock.curr_price
        invested_value = item.purchase_quantity * item.purchase_price

        total_value += stock_value
        invested += invested_value
        item.total_value = stock_value

    gains = ((total_value - invested) / invested) * 100 if invested != 0 else 0

    context = {
        'data': user_stocks,
        'total_value': total_value,
        'invested': invested,
        'gains': round(gains, 2),
    }

    # context = {'data' : user_stocks}

    return render(request , 'index.html' , context)


def getData(request):
    nasdaq_tickers = [
        "AAPL"
    #      , "GOOGL", "MSFT", "TSLA", "AMZN", "META", "NFLX", "NVDA", "INTC", "ADBE"
    ]
    headers = {
    'Content-Type': 'application/json'
    }
    token = "1d4f0a8414525ae1e92d9730681d202d7d557123"
    def getStock(ticker):
        url = f"https://api.tiingo.com/tiingo/daily/{ticker}?token={token}"
        priceurl = f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?token={token}"
        requestResponse = requests.get(url, headers=headers)
        Metadata = requestResponse.json()
        print(Metadata)
        priceData = requests.get(priceurl , headers = headers)
        print(priceData.json())
        priceData = priceData.json()[0]['close']
        stock = Stocks(ticker = Metadata['ticker'] , name = Metadata['name'] , description = Metadata['description'] , curr_price = priceData)
        stock.save()
    
    for i in nasdaq_tickers:
        getStock(i)
    return HttpResponse("Done!!")


def showStocks(request):
    stocks = Stocks.objects.all()
    context = {"data" : stocks}
    return render(request , 'market.html' , context )


def loginView(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username , password = password)
        if user:
            login(request , user)
        else:
            # raise("Invalid credentials")
            messages.error(request, "Invalid username or password")
            return redirect('login')
        
        return  redirect('home')
        
    return render(request , 'login.html')


def logoutView(request):
    logout(request)
    return redirect('login')


def registerView(request):
    if request.user:
        logout(request)

    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        phone_number = request.POST.get('phoneNumber')
        address = request.POST.get('Address')
        pancard_number = request.POST.get('pancard_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user_image = request.FILES.get('profile_pic')
        pancard_image=  request.FILES.get('pancard_image')
        if User.objects.filter(username = username).exists():
            messages.error(request , "username exists!!!")
            return render(request , 'register.html')
        
        if password1 != password2:
            messages.error(request , "Password doesnot match!!!")
            return render(request , 'register.html')
    
        
        user = User(username = username , email = email , first_name = first_name , last_name = last_name)
        user.set_password(password1)
        user.save()

        user_info = UserInfo(
            user = user ,
            phone_number = phone_number,
            address = address,
            pancard_number = pancard_number,
            user_image = user_image,
            pancard_image = pancard_image
        )

        user_info.save()

        # login(request , user)
        return redirect('login')
    return render(request , 'registerUser.html')

@login_required
def buy(request , id):
    stock = get_object_or_404(Stocks , ticker = id)
    user = request.user

    purchase_quantity = int(request.POST.get('quantity'))
    purchase_price = stock.curr_price

    userStocks =  UserStock.objects.filter(stock = stock , user = user).first()
    
    if userStocks:
        userStocks.purchase_price  = (userStocks.purchase_quantity * userStocks.purchase_price + purchase_price*purchase_quantity) / purchase_quantity+userStocks.purchase_quantity
        userStocks.purchase_quantity = userStocks.purchase_quantity + purchase_quantity
        userStocks.save()
    else :
        userStock = UserStock(
            stock = stock , 
            user = user , 
            purchase_price = purchase_price , 
            purchase_quantity = purchase_quantity
            )
        userStock.save()
    return redirect('market')

@login_required
def sell(request , id):
    stock  = get_object_or_404(Stocks , ticker = id )
    user = request.user

    sell_quantity = int(request.POST.get('quantity'))
    userStocks =  UserStock.objects.filter(stock = stock , user = user).first()
    if(sell_quantity > userStocks.purchase_quantity):
        raise("!!!SELL QUANTITY IS HIGHER!!!")
    else:
        userStocks.purchase_quantity = userStocks.purchase_quantity - sell_quantity
        if userStocks.purchase_quantity == 0:
            userStocks.delete()
        else:
            userStocks.save()
    return redirect('market')

def stock(request):
    q =request.POST.get('search')

    if q:
        stocks = Stocks.objects.filter(name__icontains=q)
    else:
        stocks = Stocks.objects.all()

    context= {'data' : stocks}
    return render(request , 'market.html' , context)

