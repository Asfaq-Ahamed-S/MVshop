from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from .models import Product,Customer,Category,CartItem,Order
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required

# Create your views here.

# Http Response
'''
def index(request):
    return HttpResponse("Hello World...Index view")

def cart(request,cart_id):   #Dynamic URL
    return HttpResponse(f"Hello World...Cart page {cart_id}")

def old_url(request):        #Redirect and reverse(using url name)
    return redirect(reverse('Shop:new_url'))

def new_url_view(request):
    return HttpResponse("This is new url")

'''
# HTML Response

def register(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        errors=[]
        if User.objects.filter(username=username).exists():
            errors.append("Username already exists")
        if User.objects.filter(email=email).exists():
            errors.append("Email already exists")
        
        if errors:
            return render(request,'register.html',{'errors':errors})
        
        user = User.objects.create_user(username=username,email=email,password=password)
        Customer.objects.create(user=user)

        login(request,user)
        return redirect('Shop:index')

    return render(request,'register.html')

def admin_register(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        new_user = User(username=username,email=email,password=password,is_superuser=1,is_staff=1)
        new_user.set_password(password)
        new_user.save()

    return render(request,'register.html')

def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('Shop:index')
        else:
            error = "Invalid username or password"
            return render(request,'login.html',{'error':error})

    return render(request,'login.html')

def user_logout(request):
    logout(request)
    return redirect('Shop:index')

def index(request):
    products = Product.objects.all()
    return render(request,'index.html',{'products':products})

def add_to_cart(request,product_id):
    if not request.user.is_authenticated:
        return redirect('Shop:login')
    
    customer = Customer.objects.get(user=request.user)
    product = get_object_or_404(Product,id=product_id )

    cart_item,created = CartItem.objects.get_or_create(customer=customer,product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('Shop:cart')

def detail(request,product_id):

    product = Product.objects.get(pk=product_id)
    products = Product.objects.all()
    return render(request,'detail.html',{'product':product,'products':products,'product_id':product_id})

def cart(request):
    if not request.user.is_authenticated:
        return redirect('Shop:login')
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user = request.user)
        
    cart_items = CartItem.objects.filter(customer=customer)
    total_price = sum(item.get_total_price() for item in cart_items)

    for item in cart_items:
        item_quantity = item.quantity
    
    if item_quantity:

        return render(request,'cart.html',{'cart_items':cart_items,'total_price':total_price,'item_quantity':item_quantity})
    else:
        return render(request,'cart.html',{'cart_items':cart_items,'total_price':total_price})


def category(request):
    categories = Category.objects.all()
    return render(request,'category.html',{'categories':categories})

def about(request):
    return render(request,'about.html')

def detail_category(request,category_id):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request,'detail_category.html',{'category_id':category_id,'products':products,'categories':categories})

def payment_success(request):
    return render(request,"payment_success.html")

def payment_cancelled(request):
    return render(request,"payment_cancelled.html")

def checkout(request):
    customer = Customer.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(customer=customer)
    total_price = sum(item.get_total_price() for item in cart_items)
    return render(request,"checkout.html",{'cart_items':cart_items,'total_price':total_price,'user':request.user})

@login_required
def process_checkout(request):
    if request.method == 'POST':
        name = request.POST['name']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip']
        payment_method = request.POST['payment-method']

        customer = Customer.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(customer=customer)

        superuser = User.objects.filter(is_superuser=True).first()

        order = Order.objects.create(
            superuser=superuser,
            user=request.user,
            shipping_address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            payment_method=payment_method
        )

        for item in cart_items:
            order.cart_items.add(item)
            print("item added successfully")

        if payment_method == 'paypal':
            return render(request,"payment.html",{'total_price':sum(item.get_total_price() for item in CartItem.objects.filter(customer=Customer.objects.get(user=request.user)))})
        elif payment_method == 'cod':
            return redirect('Shop:payment_success')
    return redirect('Shop:checkout')

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    for order in orders:
        order_items = order.cart_items.all()
        for item in order_items:
            print(f"{item.product.name}")
    return render(request,"orders.html",{'orders':orders})

@login_required
def cancel_order(request,order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.delete()
    return redirect('Shop:my_orders')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, customer=Customer.objects.get(user=request.user))
    item.delete()
    return redirect('Shop:cart')