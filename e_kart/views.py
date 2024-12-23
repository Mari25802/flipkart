from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth import authenticate,login as log_auth,logout
import json
# Create your views here.

def header(request):
    category=Category.objects.filter(status=0)
    return render(request,'e_kart/includes/header.html',{"category":category})

def index(request):
    category=Category.objects.filter(status=0)
    products=Products.objects.filter(status=0)
    return render(request, 'e_kart/index.html',{"category":category,"products":products})

def register(request):
    form=RegisterForm()
    if request.method == "POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Success You Can Login Now..!")
            return redirect('ekart:login')
    return render(request, 'e_kart/register.html',{"form":form})

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method=="POST":
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(username=name, password=pwd)
            if user is not None:
                log_auth(request,user)
                messages.success(request,"Logged in Successfully")
                return redirect('/')
                    
            else:
                messages.error(request,"Invalid User Name or Password")
                return redirect('ekart:login')   
        return render(request, 'e_kart/login.html')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Successfully")
        return redirect('/')
        
def collection(request):
    fav=Favourite.objects.filter(user=request.user)
    category=Category.objects.filter(status=0)
    return render(request, 'e_kart/collection.html',{"category":category,"fav":fav})

def collectionview(request,name):  
    category=Category.objects.filter(status=0)
    fav=Favourite.objects.filter(user=request.user)
    
    if(Category.objects.filter(name=name ,status=0)):
        products=Products.objects.filter(category__name=name)
        return render(request,'e_kart/product.html',{"products":products , "category_name":name,"category":category,"fav":fav})
    else:
        messages.warning(request,'No such category found')
        return redirect('collection')

def product_details(request,cname,pname):
    fav=Favourite.objects.filter(user=request.user)
    category=Category.objects.filter(status=0)
    if(Category.objects.filter(name=cname , status=0)):
        if(Products.objects.filter(name=pname, status=0)):
            product=Products.objects.filter(name=pname, status=0).first()
            return render(request, 'e_kart/product_details.html',{"product":product,"category":category,"fav":fav})
        else:
            messages.warning(request,'No such category found')
            return redirect('collection')  
    else:
        messages.error(request, "No such category found")
        return redirect('index')

def fav_page(request):
    if request.headers.get('x-Request-with')=="XMLHttpRequest":
        if request.user.is_authenticated:
            data=json.load(request)
            product_id=data['product_id']
            product_status=Products.objects.get(id=product_id)
            if product_status:
                if Favourite.objects.filter(user=request.user.id, product_id=product_id):
                    return JsonResponse({'status':"Product already in fav"},status=200)
                else:
                    Favourite.objects.create(user=request.user,product_id=product_id)
                    return JsonResponse({'status':"Product added to fav"},status=200)
        else:
            return JsonResponse({'status':'Login'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
         
def cart(request):
    
    if request.headers.get('x-Request-with')=="XMLHttpRequest":
        if request.user.is_authenticated:
            data=json.load(request)
            product_id=data['product_id']
            product_qty=data['product_qty']
            print(request.user.id)
            product_status=Products.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id, product_id=product_id):
                    return JsonResponse({'status':"Product already in cart"},status=200)
                else:
                    if product_status.quantity>= product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':"Product added to cart"},status=200)
                    else:
                        return JsonResponse({'status':"Product stock not available"},status=200)
 
        else:
            return JsonResponse({'status':'Login'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
    
# cart_page
def cart_page(request):
    category=Category.objects.filter(status=0)
    fav=Favourite.objects.filter(user=request.user)

    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,'e_kart/cart.html',{"cart":cart,"category":category,"fav":fav})
    else:
        return redirect('/')

def fav_view(request):
    category=Category.objects.filter(status=0)
    
    if request.user.is_authenticated:
        fav=Favourite.objects.filter(user=request.user)
        return render(request, 'e_kart/fav.html',{"fav":fav,"category":category})
    else:
        return redirect('/')
        
def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect('/cart_page')

def remove_fav(request,fid):
    favitem=Favourite.objects.get(id=fid)
    favitem.delete()
    return redirect('/fav_view')