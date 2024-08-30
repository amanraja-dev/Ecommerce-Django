from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages  
from django.db.models import Q
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib.auth.models import User, auth
from django.core.paginator import Paginator
import random
import string
from apps.models import ADDRESS,BRAND,CATEGORIES,CART,COLOUR,PRODUCT,ORDER,WISHLIST
from django.contrib.auth.decorators import login_required


def home(request):
    man = PRODUCT.objects.filter(gender='Man')
    paginator=Paginator(man,4)
    page_number_m=request.GET.get('page')
    man=paginator.get_page(page_number_m)

    woman = PRODUCT.objects.filter(gender='Woman')
    paginator=Paginator(woman,4)
    page_number_w=request.GET.get('page')
    woman=paginator.get_page(page_number_w)

    shirt = CATEGORIES.objects.filter(categories='Shirt')
    jeans = CATEGORIES.objects.filter(categories='Jeans')
    trouser = CATEGORIES.objects.filter(categories='Trousers')
    trackpant = CATEGORIES.objects.filter(categories='Trackpants')
    shoes = CATEGORIES.objects.filter(categories='Shoes')
    wallet = CATEGORIES.objects.filter(categories='Wallet')
    watch = CATEGORIES.objects.filter(categories='Watch')
    formal_suit = CATEGORIES.objects.filter(categories='Formal suit')

    top_jeans = CATEGORIES.objects.filter(categories='Top and Jeans')
    tops = CATEGORIES.objects.filter(categories='Tops')
    salwar_suit = CATEGORIES.objects.filter(categories='Salwar suit')
    frock = CATEGORIES.objects.filter(categories='Frock')

    return render(request, "index.html",{'man':man,'woman':woman,'shirt':shirt,'jeans':jeans,'trouser':trouser,'trackpant':trackpant,'shoes':shoes,'wallet':wallet,'watch':watch,'formal_suit':formal_suit,'top_jeans':top_jeans,'tops':tops,'salwar_suit':salwar_suit,'frock':frock})

def search(request):
    if request.method== 'POST':
        search = request.POST.get('search_value')
        results = PRODUCT.objects.filter(Q(product_name__icontains=search) | Q(gender__icontains=search) | Q(categories__categories=search)| Q(colour__colour_name=search))
        data={'searchresult':results}
        return render(request, "search/search.html",data)
    return redirect('home')

def shop(request):
    shirt = CATEGORIES.objects.filter(categories='Shirt')
    jeans = CATEGORIES.objects.filter(categories='Jeans')
    trouser = CATEGORIES.objects.filter(categories='Trousers')
    trackpant = CATEGORIES.objects.filter(categories='Trackpants')
    shoes = CATEGORIES.objects.filter(categories='Shoes')
    wallet = CATEGORIES.objects.filter(categories='Wallet')
    watch = CATEGORIES.objects.filter(categories='Watch')
    formal_suit = CATEGORIES.objects.filter(categories='Formal suit')

    top_jeans = CATEGORIES.objects.filter(categories='Top and Jeans')
    tops = CATEGORIES.objects.filter(categories='Tops')
    salwar_suit = CATEGORIES.objects.filter(categories='Salwar suit')
    frock = CATEGORIES.objects.filter(categories='Frock')

    categories_product = PRODUCT.objects.filter(categories__categories = categories)
    data = {'categories_product':categories_product,'shirt':shirt,'jeans':jeans,'trouser':trouser,'trackpant':trackpant,'shoes':shoes,'wallet':wallet,'watch':watch,'formal_suit':formal_suit,'top_jeans':top_jeans,'tops':tops,'salwar_suit':salwar_suit,'frock':frock}
    return render(request, "shop/shop.html",data)

def categories(request,categories):
    categories_name = categories
    categories_product = PRODUCT.objects.filter(categories__categories = categories)
    data = {'categories_product':categories_product,'categories_name':categories_name}
    return render(request, "shop/categories.html",data)

def manshop(request):
    man = PRODUCT.objects.filter(gender='Man')
    data = {'man_products':man}
    return render(request, "shop/man.html",data)

def womanshop(request):
    woman = PRODUCT.objects.filter(gender='Woman')
    data = {'woman_products':woman}
    return render(request, "shop/woman.html",data)

def spdpage(request,product_id):
    single_product_dtls = PRODUCT.objects.filter(product_id = product_id)
    data = {'S_P_dtls':single_product_dtls}
    return render(request,"shop/details.html",data)

@login_required
def wishlist(request):
    wishlist = WISHLIST.objects.filter(user=request.user)
    data = {'wishlist_product': wishlist}
    return render(request, 'wishlist/wishlist.html', data)

@login_required
def add_to_wishlist(request):
    user = request.user
    product_id = request.POST.get('product_id')

    if product_id:
        product = PRODUCT.objects.get(product_id=product_id)
        if not WISHLIST.objects.filter(user=user, product=product).exists():
            WISHLIST(user=user, product=product).save()
            messages.success(request, "Product added to wishlist successfully!")
        else:
            messages.error(request, "Product already exists in the wishlist.")
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, product_id):
    user = request.user
    wishlist = WISHLIST.objects.filter(user=user, product__product_id=product_id)
    if wishlist.exists():
        wishlist.delete()
        messages.success(request, "Product removed from wishlist successfully!")
    else:
        messages.error(request, "Product not found in the wishlist.")
    return redirect('wishlist')

@login_required
def cart(request):
    user = request.user
    address = ADDRESS.objects.filter(user=user)
    cart_products = CART.objects.filter(user=user)
    shipping_amount = 100.00

    if cart_products.exists():
        amount = sum(p.quantity * p.product.selling_price for p in cart_products)
        total_amount = amount + shipping_amount
        return render(request, 'cart/cart.html', {'carts': cart_products, 'amount': amount, 'total_amount': total_amount, 'shipping_amount': shipping_amount, 'address': address})
    else:
        return render(request, 'cart/cart.html')

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        user = request.user
        product_id = request.POST['product_id']

        try:
            product = PRODUCT.objects.get(product_id=product_id)

            if CART.objects.filter(user=user, product_id=product_id).exists():
                messages.info(request, "This product is already in your cart.")
            else:
                CART(user=user, product=product).save()
                messages.success(request, "Product added to cart successfully.")

        except PRODUCT.DoesNotExist:
            messages.error(request, "Product does not exist.")

    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    user = request.user
    cart_item = CART.objects.filter(user=user, product__product_id=product_id)
    
    if cart_item.exists():
        cart_item.delete()
        messages.success(request, 'Item removed from cart successfully!')
    else:
        messages.error(request, 'Item not found in the cart.')
    return redirect('cart')


@login_required
def address(request):
    if request.method == "POST":
        mobile = request.POST.get('mobile')
        state = request.POST.get('state')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')

        ADDRESS.objects.create(
            user=request.user,
            mobile=mobile,
            state=state,
            city=city,
            zipcode=pincode
        )

        messages.success(request, "Address saved successfully.")
        return redirect('address')
    else:
        address = ADDRESS.objects.filter(user=request.user)
        return render(request, 'profile/address.html', {'address': address})

@login_required  
def delete_address(request,address_id):
    user=request.user
    address=ADDRESS.objects.filter(address_id=address_id)
    address.delete()
    return redirect('address')

def payment_address(request):
    if request.user.is_authenticated:
        address = ADDRESS.objects.filter(user=request.user)
        if address is not None:
            return render(request,'order/address.html',{'address':address})
        
def save_payment_address(request):
    user = request.user
    if request.method=="POST":
        mobile=request.POST['mobile']
        state=request.POST['state']
        city=request.POST['city']
        pincode=request.POST['pincode']

        user = ADDRESS(user=user,mobile=mobile,state=state,city=city,zipcode=pincode)
        user.save()

        messages.success(request, "Successfully save address.")
        return redirect('payment_address')
        
def delete_payment_address(request,address_id):
    user=request.user
    address=ADDRESS.objects.filter(address_id=address_id)
    address.delete()
    return redirect('payment_address')

# @login_required
def profile(request):
    if request.user.is_authenticated:
        user=request.user
        address = ADDRESS.objects.filter(user=user)
        data={'address':address,'user':user}
        return render(request,'profile/profile.html',data)
    return redirect('signin')

# @login_required
def orders(request):
    user=request.user
    user_order = ORDER.objects.filter(user=user)
    data={'user_order':user_order}
    return render(request,'order/order.html',data)

def podpage(request,product_id):
    user=request.user
    ordered_product_dtls = ORDER.objects.filter(product_id = product_id)
    data = {'O_P_dtls':ordered_product_dtls}
    return render(request,"order/details.html",data)

def payment(request):
    user=request.user
    custid = request.GET.get('address_id')
    address=ADDRESS.objects.get(address_id=custid)
    cart=CART.objects.filter(user=user)
    for c in cart:
        order = ORDER(user=user,address=address,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect('order')

def help(request):
    return render(request,"help/help.html")

def aboutus(request):
    return render(request,"aboutus/aboutus.html")