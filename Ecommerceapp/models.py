from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save
import uuid
from django.urls import reverse
from django.utils.safestring import mark_safe






class Main_categorie(models.Model):
    name = models.CharField(null=True,max_length=200)
    image = models.ImageField(upload_to='Main_category_images',null=True,blank=True)
    slug = models.SlugField(max_length=255,null=True, unique=True)


    def __str__(self):
        return self.name

class Categorie(models.Model):
    main_category = models.ForeignKey(Main_categorie,on_delete=models.CASCADE)
    name = models.CharField(null=True,max_length=200)
    image = models.ImageField(upload_to='Subcategory_images',null=True,blank=True)
    slug = models.SlugField(max_length=255, unique=True,null=True)


    def __str__(self):
        return self.name + " -> " + self.main_category.name

class Sub_categorie(models.Model):
    category = models.ForeignKey(Categorie,on_delete=models.CASCADE)
    name = models.CharField(null=True,max_length=200)
    slug = models.SlugField(max_length=255, unique=True,null=True)


    def __str__(self):
        return self.name +"->"+self.category.name+"->"+ self.category.main_category.name

class Coupon(models.Model):
    code = models.CharField(null=True,max_length=200)
    discount = models.IntegerField(null=True,)

    def __str__(self):
        return self.code

class Tag(models.Model):
    name = models.CharField(null=True,max_length=200)

    def __str__(self):
        return self.name
    

# class Color (models.Model):
# name = models.CharField(max_length=20)
# code = models.CharField(max_length=10, blank=True, null=True)
# def _str__(self):
# return self.name
# def color_tag(self):
# if self.code is not None:
# else:
# return mark_safe('<p style="background-color: {}">Color </p>'.format(self.code))
# return ""
# class Size (models.Model):
# name = models.CharField(max_length=20)
# code = models.CharField(max_length=10, blank=True, null=True)
# def _str__(self):
# return self.name


class Color(models.Model):
    code = models.CharField(null=True,max_length=100)
    name = models.CharField(max_length=20)
  
    
    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color: {}">Color </p>'.format(self.code))
        else:
            return ""
    
    def _str__(self):
        return self.name
    
class Size(models.Model):
    name = models.CharField(null=True,max_length=200)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name




class Partners(models.Model):
    name = models.CharField(null=True,max_length=100)
    image = models.ImageField(null=True,)

    def __str__(self):
        return self.name


class  Brands(models.Model):
    Brand_name=models.CharField(null=True,max_length=100)
    image = models.ImageField(upload_to='Brand_images',null=True,blank=True)
    

    def __str__(self):
        return self.Brand_name
    
class Moving_text(models.Model):
    text = models.CharField(null=True,max_length=300)
    date=models.DateTimeField(null=True,default=timezone.now)

    def __str__(self):
        return self.date +"->"+ self.text
    

class Discount_deal(models.Model):
    name = models.CharField(null=True,max_length=200)

    def __str__(self):
        return self.name

class Sliders(models.Model):


    Image = models.ImageField(null=True,upload_to='slider_imgs')
    Discount_deal = models.ForeignKey(Discount_deal,on_delete=models.CASCADE)
    Sale = models.IntegerField(null=True,)
    Brand_name = models.CharField(null=True,max_length=200)
    Discount = models.IntegerField(null=True)
    Description = models.CharField(null=True,max_length=100)
    Link = models.CharField(null=True,max_length=2000)

    def __str__(self):
        return self.Brand_name

class Header_Icons(models.Model):
    Category = models.ForeignKey(Categorie,on_delete=models.CASCADE,null=True)
    # name = models.CharField(max_length=200,null=True)
    Icon = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.Category.name


class Section(models.Model):
    name = models.CharField(null=True,max_length=150)

    def __str__(self):
        return self.name
    
class Banners(models.Model):


    image = models.ImageField(null=True,upload_to='sm_banners')
    Key_point_2 = models.CharField(null=True,max_length=100)
    Discount_deal = models.ForeignKey(Discount_deal, on_delete=models.CASCADE,null=True,)
    Key_point_1 = models.CharField(null=True,max_length=200)
    Discount = models.IntegerField(null=True,blank=True)
    Link = models.CharField(max_length=2000,null=True,blank=True)
    section = models.ForeignKey(Section,null=True,on_delete=models.CASCADE)
    category = models.ForeignKey(Categorie,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.Key_point_2

    


class Product(models.Model):
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    name = models.CharField(null=True, max_length=120)
    # image = models.ImageField(null=True, upload_to='Product_images')
    image = models.ImageField(blank=True,null=True,upload_to='Product_images')
    total_quantity = models.IntegerField(null=True)
    Availability = models.IntegerField(null=True)
    price = models.FloatField(null=True)
    Discount = models.IntegerField(null=True)
    tax = models.FloatField(null=True, blank=True)
    packing_cost = models.FloatField(null=True, blank=True)
    Product_info = RichTextField(null=True)
    model_name = models.CharField(null=True, max_length=120)
    Category = models.ForeignKey('Categorie', null=True, on_delete=models.CASCADE)
    Sub_category = models.ForeignKey('Sub_categorie', on_delete=models.CASCADE, null=True, blank=True)
    Tags = models.ForeignKey('Tag', null=True, blank=True, on_delete=models.CASCADE)
    color = models.ForeignKey('Color', null=True, blank=True, on_delete=models.SET_NULL)
    size = models.ForeignKey('Size', null=True, blank=True, on_delete=models.SET_NULL)
    Description = RichTextField(null=True)
    Section = models.ForeignKey('Section', null=True, on_delete=models.DO_NOTHING)
    brand = models.ForeignKey('Brands', on_delete=models.CASCADE, null=True, blank=True)

    def variants(self):
        # Return the variants related to this product
        return Variants.objects.filter(product=self)
    
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url) if self.image else '')

    image_tag.short_description = 'Image'
  

    def quantity_sold(self):
        return self.total_quantity - self.Availability

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Your existing save logic
        if not self.slug:
            self.slug = self.generate_custom_id()
        super().save(*args, **kwargs)

    def generate_custom_id(self):
        # Your existing custom ID generation logic
        # For example, combining time and random characters
        from django.utils.crypto import get_random_string
        current_time = timezone.now()
        timestamp_milliseconds = int(current_time.timestamp() * 1000)
        
        # Modify this part according to your needs
        sliced_name = self.name.split()[0]
        return f"ESP{slugify(sliced_name)}PTD{timestamp_milliseconds}_{get_random_string(5)}"
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={'slug': self.slug})

    def custom_id(self):
        return f"Custom ID: {self.slug}"

    # ... other methods ...

    class Meta:
        db_table = "app_Product"


# def create_slug(instance, new_slug=None):
#     slug = slugify(instance.name)
#     if new_slug is not None:
#         slug = new_slug
#     qs = Product.objects.filter(slug=slug).order_by('-id')
#     exists = qs.exists()
#     if exists:
#         new_slug = "%s-%s" % (slug, qs.first().id)
#         return create_slug(instance, new_slug=new_slug)
#     return slug

# def pre_save_post_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = create_slug(instance)

# pre_save.connect(pre_save_post_receiver, Product)

    


class Additional_info(models.Model):
    product = models.ForeignKey(Product,null=True,on_delete=models.CASCADE)
    specification = models.CharField(null=True,max_length=120)
    detail = models.CharField(null=True,max_length=100)

    def __str__(self):
        return self.product.name
    
class Product_image(models.Model):
    product = models.ForeignKey(Product,null=True,on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to='Product_images')

    def __str__(self):
        return f"{self.product.name} - Image {self.id}"
    


# VARIANTS
class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, blank=True, null=True)
    image_id = models.IntegerField(blank=True, null=True, default=0)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(default=0)

    def __str__(self):
        return self.title

    def image(self):
        img = Product_image.objects.get(id=self.image_id)
        return img.image if img.id is not None else None

    @property
    def color_name(self):
        return self.color.name if self.color else ''

    def image_tag(self):
        img = Product_image.objects.get(id=self.image_id)
        if img.id is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""
        
    @classmethod
    def create_variant(cls, product, title, color, size, image_id, quantity, price):
        # Create a new variant based on the given product
        return cls.objects.create(
            title=title,
            product=product,
            color=color,
            size=size,
            image_id=image_id,
            quantity=quantity,
            price=price
        )


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return self.user.email
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.cart.user.email +'->'+self.product.name
    


class Comment(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    numeric_rating = models.IntegerField(default=0, choices=[(i, i) for i in range(1, 6)])
    image = models.ImageField(upload_to='comment_images', null=True, blank=True)

class Rating(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.stars} stars"

    class Meta:
        unique_together = ['product', 'user']


class Contact(models.Model):
    contact_id=models.AutoField(primary_key=True)
    email=models.EmailField(null=True,)
    name=models.CharField(null=True,max_length=50)
    subject=models.CharField(null=True,max_length=500)
    message=models.TextField(null=True,max_length=1000)
    email=models.EmailField(null=True,max_length=20)


    def __str__(self):
        return self.email



class Order(models.Model):
    user=models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    ordered_product = RichTextField(null=True)
    paid=models.BooleanField(default=False,null=True)
    firstname=models.CharField(null=True,max_length=200)
    lastname=models.CharField(null=True,max_length=200)
    email = models.EmailField(null=True,max_length=90)
    address = models.TextField(null=True,)
    city = models.CharField(null=True,max_length=100)
    # state = models.CharField(null=True,max_length=100)
    zip_code = models.CharField(null=True,max_length=100)
    additional_info=models.TextField(null=True,)
    date=models.DateTimeField(null=True,default=timezone.now)
    phone = models.CharField(null=True,max_length=20)
    amount=models.CharField(null=True,max_length=100)
    payment_id=models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.email

class Order_item(models.Model):
    order=models.ForeignKey(Order,null=True,on_delete=models.CASCADE)
    product=models.CharField(null=True,max_length=200)
    image=models.ImageField(null=True,upload_to='Order_item')
    quantity=models.IntegerField(null=True,)
    price=models.CharField(null=True,max_length=150)
    total=models.CharField(null=True,max_length=180)

    def __str__(self):
        return self.order.user.username

class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(null=True,default="")
    update_desc = models.CharField(null=True,max_length=5000)
    delivered=models.BooleanField(null=True,default=False)
    timestamp = models.DateField(null=True,auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."

