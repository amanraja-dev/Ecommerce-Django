"""
URL configuration for Ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views , auth_views , authentication_view 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Custom URLs
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),

    # Authentication URLs
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('signup/', authentication_view.signup, name='signup'),
    path('signup-otp/', authentication_view.verify_signup_otp, name='signup_otp'),
    path('signin/', authentication_view.signin, name='signin'),
    path('logout/', authentication_view.logout_user, name='logout'),
    
    # Password reset URLs
    path('forget-password/', auth_views.forget_password, name='forget_password'),
    path('reset-password-otp/', auth_views.reset_password_otp, name='reset_password_otp'),
    path('verify-reset-password-otp/', auth_views.verify_reset_password_otp, name='verify_reset_password_otp'),

    
    # Product URLs
    path('categories/<str:categories>/', views.categories, name='categories'),
    path('shop/', views.shop, name='shop'),
    path('manshop/', views.manshop, name='manshop'),
    path('womanshop/', views.womanshop, name='womanshop'),
    path('spdpage/<uuid:product_id>/', views.spdpage, name='spdpage'),
    path('podpage/<uuid:product_id>/', views.podpage, name='podpage'),

    # User Profile and Order URLs
    path('profile/', views.profile, name='profile'),
    path('order/', views.orders, name='order'),
    path('payment/', views.payment, name='payment'),

    # Cart and Wishlist URLs
    path('cart/', views.cart, name='cart'),
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('remove/<uuid:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('addtowishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('removewish/<uuid:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    # Address URLs
    path('address/', views.address, name='address'),
    path('deleteaddress/<uuid:address_id>/', views.delete_address, name='delete_address'),
    
    path('paddress/', views.payment_address, name='payment_address'),
    path('savepaddress/', views.save_payment_address, name='save_payment_address'),
    path('deletepaddress/<uuid:address_id>/', views.delete_payment_address, name='delete_payment_address'),

    # Other URLs
    path('help/', views.help, name='help'),
    path('aboutus/', views.aboutus, name='aboutus'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)