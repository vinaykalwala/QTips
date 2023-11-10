from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from .models import *
import admin_thumbnails

class OrderItemInline(admin.TabularInline):
    model = Order_item

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
@admin_thumbnails.thumbnail('image',)
class ProductImageInline(admin.TabularInline):
    model = Product_image
    # readonly_fields = ('id',)
    extra=1

class AdditionalInfoInline(admin.TabularInline):
    model = Additional_info

class VariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ['image_tag'] # Make sure to include the readonly field for image_tag
    def image_tag(self, obj):
        if obj.image_id:
            img = Product_image.objects.get(id=obj.image_id)
            return format_html('<img src="{}" height="60" />', img.image.url)
        return None

    readonly_fields = ('image_tag',)

    extra = 1
    show_change_link = True


class ProductsAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, VariantsInline, AdditionalInfoInline]
    list_display = ('name','display_image', 'price', 'Category', 'Sub_category', 'Section')
    list_editable = ('Category', 'Sub_category', 'Section')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('display_image',)  # Use a custom method instead

    def display_image(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.image.url)

    display_image.short_description = 'Image'

@admin_thumbnails.thumbnail('image',)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name']

    def product_name(self, obj):
        return obj.product.name if obj.product else ''
    
    product_name.short_description = 'Product Name'
# admin.site.register(Product_image, ImageAdmin)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'color_tag']

    @property
    def name(self):
        return self.name if self.color else ''

class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']

class VariantsAdmin(admin.ModelAdmin):
     list_display = ['title', 'product', 'color_name', 'size', 'price', 'quantity', 'image_tag']
# Partners
admin.site.register(Partners)

# Register your models here.
admin.site.register(Contact)
admin.site.register(OrderUpdate)
admin.site.register(Discount_deal)
admin.site.register(Order, OrderAdmin)
admin.site.register(Tag)
# admin.site.register(Order_item)
admin.site.register(Brands)
admin.site.register(Sliders)
admin.site.register(Header_Icons)
admin.site.register(Banners)

# CATEGORIES
admin.site.register(Main_categorie)
admin.site.register(Categorie)
admin.site.register(Sub_categorie)

# PRODUCTS & VIEWS
admin.site.register(Product, ProductsAdmin)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Product_image,ImageAdmin)
admin.site.register(Additional_info)
admin.site.register(Section)
admin.site.register(Size, SizeAdmin)
admin.site.register(Variants, VariantsAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Coupon)

# CART
admin.site.register(Cart)
admin.site.register(CartItem)
