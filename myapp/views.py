from datetime import datetime
from django.conf import  settings
from django.contrib import auth
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

from .models import Category, Product, Client, Order
from django.shortcuts import get_object_or_404, render, redirect
import django.http
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import OrderForm, InterestForm
from django.db import connection

def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    if 'last_login' in request.session:
        last_login = request.session['last_login']
    else:
        last_login = 'Your last login was more than one hour ago'
    return render(request, 'myapp/index.html', {'cat_list': cat_list, 'last_login': last_login})



def about(request):
    # return HttpResponse('This is an Online Store APP.')
    if 'about_visits' in request.session:
        request.session['about_visits'] += 1
    else:
        request.session['about_visits'] = 1
        request.session.set_expiry(300)

    return render(request, 'myapp/about.html', {'about_visits': request.session['about_visits']})


def detail(request, cat_no):
    cat_requested = get_object_or_404(Category, id=cat_no)
    Products = Product.objects.filter(category=cat_requested)

    response = HttpResponse()
    para1 = '<p>' + str(cat_requested.warehouse) + '</p>'
    response.write(para1)

    heading1 = '<br> <p>' + ' Result: ' + '</p>'
    response.write(heading1)
    return render(request, 'myapp/detail.html', {'products': Products, 'warehouse': cat_requested.warehouse})

def products(request):
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request, 'myapp/products.html', {'prodlist': prodlist})

def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:
                obj = prodlist.get(id=order.product.id)
                obj.stock = obj.stock - order.num_units
                obj.save()
                order.save()
                msg = 'Your order has been placed successfully.'
            else:
                msg = 'We do not have sufficient stock to fill your order.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'prodlist': prodlist})


def productdetail(request, prod_id):
    msg = ''
    prod: Product = Product.objects.filter(id=prod_id).get()
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            # Check Interest
            if form.cleaned_data['interested'] == '1':
                msg = 'You are interested'
                prod.interested += 1
                prod.save()
            else:
                msg = 'You are not interested'
            return redirect('../../myapp/')
    else:
        form = InterestForm()
    return render(request, 'myapp/productdetail.html', {'form': form, 'prod': prod, 'msg': msg})

def user_login(request):
    logout(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
       # print(user, 'login')
        if user:
            if user.is_active:
                login(request, user)
                request.session['last_login'] = str(datetime.now())
                request.session.set_expiry(3600) #AS ITS 1 HOUR 60 * 60
                #print(request.path, 'login')
                if 'myorders' in request.META.get('HTTP_REFERER'):
                    return HttpResponseRedirect(reverse('techavant:myorders'))
                return HttpResponseRedirect(reverse('techavant:index'))
            else:
                return HttpResponse('you are no longer an active user.')
        else:
            return HttpResponse('Provided credentials are invalid.')
    else:
        return render(request, 'myapp/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('techavant:index')))

def test(request):
    if request.method == 'POST':
        username = request.POST['user']
        print(username, "testing post function")

    return render(request, 'myapp/test.html')

@login_required(login_url='/myapp/login/')
def myorders(request):
    #request.user.username = ''

    try:
        client = Client.objects.get(username=request.user.username)
    except Client.DoesNotExist:
        print('Not exists')
        client = None
    print(client)
    print(request.user.username)
    if not client:
        print('not a client')
        return render(request, 'myapp/login.html', {'error_message': 'You are not registered client!'})

    orders = Order.objects.filter(client=client)
    if not orders:
        print('Inside')
        return render(request, 'myapp/myorders.html', {'error_message': 'Your orders seems empty.'})
    return render(request, 'myapp/myorders.html', {'orders':orders})


def register(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        try:
            client = get_object_or_404(Client, username=username)
        except:
            client = None

        if not username or not password:
            return render(request, 'myapp/register.html',
                          {'error_message': 'Please enter the username or password'})

        if client:
            return render(request, 'myapp/register.html',
                          {'error_message': 'Username taken Please try with another username'})

        client = Client.objects.create_user(username=username, password=password, email=email)
        client.first_name = username
        client.save()

        return redirect(reverse('techavant:login') + f'?username={username}')
    return render(request, 'myapp/register.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        client = Client.objects.get(email=email)

        if client:
            random_password = Client.objects.make_random_password()
            # print(random_password)
            client.set_password(random_password)
            client.save()
            subject = f'Hi {client.first_name}: Here is your new password'
            message = f'Your new password is: {random_password}. Please change your password from myaccount page'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [client.email]
            send_mail( subject, message, from_email, recipient_list)
        return redirect('techavant:login')

    return render(request, 'myapp/forgot_password.html')

def json(request):
    data = list(Client.objects.values())
    return JsonResponse(data, safe=False)