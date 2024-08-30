from apps.models import ADDRESS,BRAND,CATEGORIES,CART,COLOUR,FEATURED_PRODUCT,PRODUCT,ORDER,WISHLIST
from django.contrib import admin



admin.site.register(BRAND)
admin.site.register(CATEGORIES)
admin.site.register(CART)
admin.site.register(COLOUR)
admin.site.register(WISHLIST)

@admin.register(ADDRESS)
class Address_admin(admin.ModelAdmin):
    list_display=['user','mobile','state','city','zipcode',]
    search_fields=['user',]

@admin.register(FEATURED_PRODUCT)
class Featured_admin(admin.ModelAdmin):
    list_display=['product_name','gender','categories','colour','brand','selling_price',]

@admin.register(PRODUCT)
class Product_admin(admin.ModelAdmin):
    list_display=['product_name','gender','categories','colour','brand','selling_price',]
    search_fields=['product_name','gender',]
    list_filter=['gender','categories','product_name',]

@admin.register(ORDER)
class Order_admin(admin.ModelAdmin):
    list_display=['user','address','product','orderdate','status',]
    search_fields=['user',]
    list_filter=['orderdate','status',]

