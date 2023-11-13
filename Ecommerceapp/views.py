from django.http import JsonResponse
from math import ceil
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from Ecommerceapp.models import *
from django.db.models import Q
from django.db.models import F
from django.urls import reverse
from django.db.models import Avg
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.core.mail import EmailMessage,send_mail
from math import ceil
from django.template.loader import render_to_string, get_template
from Ecommerceapp import keys
from django.conf import settings
from django.contrib.auth.decorators import login_required
from CART.models import *
from cart.cart import Cart
import razorpay
from django.db.models import Min,Max,Sum
client=razorpay.Client(auth=("rzp_test_jTenA9rtqgpQjd", "7gYa1enM8ie1fCy5ACKjnQ01"))


def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')

    allProducts = Product.objects.all().distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(Categories__id__in=categories).distinct()

    if len(brands) > 0:
        allProducts = allProducts.filter(Brand__id__in=brands).distinct()


    t = render_to_string('ajax/product.html', {'products': allProducts})

    return JsonResponse({'data': t})

def cart_function(request):
    cart = Cart(request)
    cart_products = []
    for item in cart.cart:
        cart_products.append(int(item))

    return cart_products

def categories_function(request):
    main_category = Main_categorie.objects.all().order_by()
    category = Categorie.objects.all().order_by('-id')
    Sub_category = Sub_categorie.objects.all().order_by('-id')

    return main_category,category,Sub_category

def index(request):
    current_page = 'home'

    # Banners
    Slider_imgs = Sliders.objects.all().order_by('-id')
    # banner_1 = Banners.objects.filter(section__name="Home_1").order_by('-id')
    banner_1 = Banners.objects.filter(section__name="Home_1").order_by('-id')
    banner_2 = Banners.objects.select_related('category').filter(section__name="Home_2").order_by('-id')
    banner_3 = Banners.objects.select_related('category').filter(section__name="Home_3").order_by('-id')
    # Banners=Banners.objects.all().order_by('-id')
    # 
    main_category, category, Sub_category = categories_function(request)
    # products = Product.objects.filter(Section__name = 'New Arival')
    partners = Partners.objects.all().order_by('-id')
    products = Product.objects.all()
    # most_selling_products = Product.objects.annotate(quantity_sold=F('total_quantity') - F('Availability')).order_by('-quantity_sold')[:6]
    most_selling_products = Product.objects.annotate(quantity_sold=F('total_quantity') - F('Availability')).order_by('-quantity_sold')[:10]
    home_and_kitchen = Product.objects.filter(Section__name="Home & Kitchen")
    top_featured_product = Product.objects.filter(Section__name="Top Featured Product")
    top_featured_product_4 = Product.objects.filter(Section__name="Top Featured Product")[1:5]
    top_discount_products = Product.objects.order_by('-Discount')[:10]
    

    cart_products = cart_function(request)


    params= {
        'Slider_imgs' : Slider_imgs,
        'banner_1' : banner_1,
        'banner_2' : banner_2,
        'banner_3' : banner_3,
        'main_category':main_category,
        'category':category,
        'Sub_category':Sub_category,
        'products' : products,
        'partners':partners,
        'most_selling_products':most_selling_products,
        'home_and_kitchen':home_and_kitchen,
        'top_featured_product':top_featured_product,
        'top_featured_product_4':top_featured_product_4,
        'top_discount_products':top_discount_products,
        'cart_products':cart_products,
        'current_page':current_page,
    }

    return render(request,'../templates/Main/index.html',context=params)


def rate_product(request, slug):
    if request.method == 'POST':
        stars = request.GET.get('stars')
        product = Product.objects.get(slug=slug)
        user = request.user

        # Create or update the user's rating
        rating, created = Rating.objects.update_or_create(
            product=product, user=user, defaults={'stars': stars}
        )

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
        

def add_comment(request, slug):
    product = Product.objects.get(slug=slug)
    user = request.user
    content = request.POST.get('content')

    Comment.objects.create(product=product, user=user, content=content)
    return JsonResponse({'status': 'success'})


def contact(request):
    current_page = 'contact'
    if request.method=="POST":
        user_name=request.POST.get("name")
        user_email=request.POST.get("femail")
        user_subject=request.POST.get("subject")
        user_message=request.POST.get("message")
        myquery=Contact(name=user_name,subject=user_subject,email=user_email,message=user_message)
        contact_subject=user_subject
        contact_message=user_message
        email_from=settings.EMAIL_HOST_USER
        send_mail(contact_subject,contact_message,email_from,[user_email])
        myquery.save()
        messages='We will meet you soon...'
        params={
            'messages':messages,
            'current_page':current_page,

        }
        return render(request,"message_sent.html",params)

    return render(request,'../templates/Main/contact.html',{'current_page':current_page})

def ABOUT(request):
    current_page = 'about'
    params = {
                'current_page':current_page,

    }

    return render(request,'../templates/Main/about.html',context=params)

def PRODUCTS(request):
    current_page = 'shop'
    params={}
    if request.method == 'POST':
        # Get filter parameters from the form
        brands=Brands.objects.all()
        products=Product.objects.all()
        size=Size.objects.all()
        color=Color.objects.all()
        params['brands']=brands
        
        params['size']=size
        params['color']=color
        SUBCATIDURL=request.POST.get('sub_category_url')
        SUBCATID=request.POST.get('sub_category_')
       
        min_price = request.POST.get('min_price', 0)
        max_price = request.POST.get('max_price', float('inf'))
        min_price = float(min_price) if min_price is not None and min_price != '' else 0
        max_price = float(max_price) if max_price is not None and max_price != '' else float('inf')
        if max_price >= 100000:
            max_price = float('inf')
        
        selected_colors_list = request.POST.getlist('color')
        selected_sizes_list = request.POST.getlist('size')
        selected_brands_list = request.POST.getlist('brands')

        # Convert the received values to integers
        selected_colors = [int(color_id) for color_id in selected_colors_list]
        selected_sizes = [int(size_id) for size_id in selected_sizes_list]
        selected_brands = [int(brand_id) for brand_id in selected_brands_list]

        # Filter products based on selected options
       
        if SUBCATID:
            products = Product.objects.filter(
                price__range=(min_price, max_price),
                color__in=selected_colors if selected_colors else Color.objects.values_list('id', flat=True),
                size__in=selected_sizes if selected_sizes else Size.objects.values_list('id', flat=True),
                brand__id__in=selected_brands if selected_brands else Brands.objects.values_list('id', flat=True),
                Sub_category=SUBCATID
            )
            params['products']=products


            products_sub = Product.objects.filter(Sub_category=SUBCATID)
            unique_brands = set()
            unique_colors = set()
            unique_size = set()
            for product in products_sub:
                unique_brands.add(product.brand)
                unique_colors.add(product.color)
                unique_size.add(product.size)
            params['unique_brands']=unique_brands
            params['unique_colors']=unique_colors 
            params['unique_size']=unique_size
            params.pop('brands')
            params.pop('size')
            params.pop('color')
            params['subcategory_']=SUBCATID

        elif SUBCATIDURL:
            products = Product.objects.filter(
                price__range=(min_price, max_price),
                color__in=selected_colors if selected_colors else Color.objects.values_list('id', flat=True),
                size__in=selected_sizes if selected_sizes else Size.objects.values_list('id', flat=True),
                brand__id__in=selected_brands if selected_brands else Brands.objects.values_list('id', flat=True),
                Sub_category=SUBCATIDURL
            )
            params['products']=products
            products_sub = Product.objects.filter(Sub_category=SUBCATIDURL)
            unique_brands = set()
            unique_colors = set()
            unique_size = set()
            for product in products_sub:
                unique_brands.add(product.brand)
                unique_colors.add(product.color)
                unique_size.add(product.size)
            params['unique_brands']=unique_brands
            params['unique_colors']=unique_colors 
            params['unique_size']=unique_size 
            params.pop('brands')
            params.pop('size')
            params.pop('color')
            params['subcategory_']=SUBCATIDURL

    # added_to_cart = [msg for msg in messages.get_messages(request) if msg.message.startswith('Added')]

        cart = Cart(request)
        cart_products = []
        for item in cart.cart:
            cart_products.append(int(item))

        params['products']=products
        params['cart_products']=cart_products
        # Render the template with the filtered products
        return render(request, 'Main/shop.html', context=params)

    brands=Brands.objects.all()
    products=Product.objects.all()
    category=Categorie.objects.all()
    subcategory = Sub_categorie.objects.all()    
    size=Size.objects.all()
    color=Color.objects.all()
    params['brands']=brands
    params['products']=products  
    params['size']=size 
    params['color']=color 
    CATID=request.GET.get('categories')
    MAIN_CATID=request.GET.get('main_categories')
    SUBCATID=request.GET.get('sub_category')
    BRAND_ID=request.GET.get('brands')
    if CATID:
        products = Product.objects.filter(Category=CATID)
        params['products']=products
        subcategory = Sub_categorie.objects.filter(category=CATID)
    if SUBCATID:
        products = Product.objects.filter(Sub_category=SUBCATID)
        params['products']=products
        unique_brands = set()
        unique_colors = set()
        unique_size = set()
        for product in products:
            unique_brands.add(product.brand)
            unique_colors.add(product.color)
            unique_size.add(product.size)
        params['unique_brands']=unique_brands
        params['unique_colors']=unique_colors 
        params['unique_size']=unique_size 
        params.pop('brands') 
        params.pop('size') 
        params.pop('color') 

    # added_to_cart = [msg for msg in messages.get_messages(request) if msg.message.startswith('Added')]

    cart = Cart(request)
    cart_products = []
    for item in cart.cart:
        cart_products.append(int(item))

    main_category, category, Sub_category = categories_function(request)
    params.update({
        "main_category":main_category,
        'Sub_category':Sub_category,
        'category':category
    })

    
    params['category']=category
    params['subcategory']=subcategory
    params['cart_products']=cart_products
    params['current_page']=current_page,

    
    return render(request,'../templates/Main/shop.html',context=params)



def CATS(request):
    current_page = 'shop'

    brands=Brands.objects.all()
    products=Product.objects.all()
    main_category = Main_categorie.objects.all()
    category=Categorie.objects.all()
    sub_category = Sub_categorie.objects.all()

    CATID=request.GET.get('categories')

    MAIN_CATID=request.GET.get('main_categories')

    BRAND_ID=request.GET.get('brands')

    Header_icons = Header_Icons.objects.all()[:7]
    
    if CATID:
        sub_category = Sub_categorie.objects.filter(Category=CATID)

    if BRAND_ID:
        products = Product.objects.filter(brand=BRAND_ID)
    if MAIN_CATID:
        category = Categorie.objects.filter(main_category=MAIN_CATID)



   
    params= {
        'products':products,     
        'category':category,
        'brands':brands,
        'sub_category':sub_category,
        'main_category':main_category,
        "Header_icons":Header_icons,
        'current_page':current_page,

             }

    
    return render(request,'../templates/Main/cats.html',context=params)


def SUBCATS(request):
    current_page = 'shop'

    brands=Brands.objects.all()
    products=Product.objects.all()
    category=Categorie.objects.all()[:1]
    CATID=request.GET.get('categories')
    SUBCATID=request.GET.get('sub_category')

    Header_icons = Header_Icons.objects.all()[:7]
    BRAND_ID=request.GET.get('brands')
    if CATID:
        products = Product.objects.filter(Category=CATID)
        sub_category = Sub_categorie.objects.filter(category=CATID)
    if BRAND_ID:
        products = Product.objects.filter(brand=BRAND_ID)
        sub_category = Sub_categorie.objects.filter(category=CATID)
    if SUBCATID:
        products = Product.objects.filter(Sub_category=SUBCATID)
        sub_category = Sub_categorie.objects.filter(category=CATID)
    params= {
        'products':products,     
        'category':category,
        'brands':brands,
        'sub_category':sub_category,
        'Header_icons':Header_icons,
        'current_page':current_page,

             }

    
    return render(request,'../templates/Main/sub_cats.html',context=params)





@login_required(login_url="/auth/login")
def cart_add(request,slug):
    cart = Cart(request)
    product = Product.objects.get(slug=slug)
    cart.add(product=product)

    return redirect(reverse('product_detail', kwargs={'slug': slug}))


@login_required(login_url="/auth/login")
def cart_add_home(request,slug):
    cart = Cart(request)
    product = Product.objects.get(slug=slug)
    cart.add(product=product)

    # return redirect(reverse('product_detail', kwargs={'slug': slug}))
    return redirect('/')


@login_required(login_url="/auth/login")
def cart_add_shop(request,slug):
    cart = Cart(request)
    product = Product.objects.get(slug=slug)
    cart.add(product=product)

    return redirect('/products/')


@login_required(login_url="/auth/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/auth/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/auth/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/auth/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/auth/login")
def cart_detail(request):
    cart = request.session.get('cart')
    # packing_cost = sum(i['packing_cost'] for i in cart.values() if i)
    packing_cost = 0
    for i in cart.values():
        c=i['packing_cost']
        packing_cost += c
    tax=0
    for i in cart.values():
        c=i['price']*i['tax']/100
        tax += c

    coupon= None
    valid_coupon = None
    invalid_coupon = None
    if request.method == 'GET':
        coupon_code = request.GET.get('coupon_code')

        if coupon_code:
            try:
                coupon = Coupon.objects.get(code = coupon_code)
                valid_coupon = "Is a valid coupon code"
            except:
                invalid_coupon = "Invalid coupon code"

    params = {
        'packing_cost':packing_cost,
        'tax':tax,
        'coupon':coupon,
        'valid_coupon':valid_coupon,
        'invalid_coupon':invalid_coupon,
    }
    return render(request, 'cart/cart_detail.html',context=params)


def is_valid_number(term):
    try:
        float(term)
        return True
    except ValueError:
        return False


def Search(request):
    searched_query = request.GET.get('query_pass')

    # Split the search query into individual words
    search_terms = searched_query.split()

    # Create a Q object to combine multiple OR conditions
    q_objects = Q()

    # Add conditions for each word in the search query
    for term in search_terms:
        q_objects |= (
    Q(title__icontains=term) |
    Q(color__name__icontains=term) |  # Assuming color has a name field
    Q(size__name__icontains=term) |   # Assuming size has a name field
    Q(product__Category__name__icontains=term) |  # Assuming Category is a ForeignKey in Product model
    Q(product__Sub_category__name__icontains=term) |  # Assuming Sub_category is a ForeignKey in Product model
    Q(product__brand__Brand_name__icontains=term) |  # Assuming brand is a ForeignKey in Product model
    Q(product__Tags__name__icontains=term) |  # Assuming Tags is a ForeignKey in Product model
    (Q(product__price__lte=float(term)) if is_valid_number(term) else Q()) |
    (Q(product__Discount__gte=float(term)) if is_valid_number(term) else Q())
)


    # Use the Q object in the filter to get relevant variants
    variants = Variants.objects.filter(q_objects).distinct()

    related_colors = variants.values_list('color__code', flat=True).distinct()

    params = {
        'variants': variants,
        'related_colors': related_colors,
    }

    return render(request, 'Main/search.html', context=params)




def prod_detail(request, slug,variant_id=None, color=None, size=None):
    product = get_object_or_404(Product, slug=slug)
    variant = Variants.objects.filter(product=product).first()
    if variant_id:
        variant = Variants.objects.get(id=variant_id)
    
    comments = Comment.objects.filter(product=product)
    avg_rating = comments.aggregate(avg_rating=models.Avg('numeric_rating'))['avg_rating']
    user_rating = None  # You can implement this based on user authentication
    variants = Variants.objects.filter(product=product)
    
    # Adjust this based on your logic
    
    variant_details = [
        {
            'id': variant.id,
            'title': variant.title,
            'color_name': variant.color.name if variant.color else '',
            'size': variant.size.name if variant.size else '',
            'price': variant.price,
            'image_url': variant.image_id.url if variant and variant.image_id else '',
        }
    ]

    product_variant = variant_details[0]
    variant_images = Variant_image.objects.filter(variant=product_variant['id'])
    user = request.user
    user_cart = get_object_or_404(User_Cart, user=user)
    cart_items = user_cart.cart_items.all()

    cart_products = []
    for item in cart_items:
        cart_products.append({
            'id':item.variant.id,
            'variant_title': item.variant.title,
            'variant_price': item.variant.price,
            'variant_image_url': item.variant.image_id.url if item.variant.image_id else '',
            'variant_size': item.variant.size.name if item.variant.size else '',
            'variant_color': item.variant.color.name if item.variant.color else '',
            'product_id': item.variant.product.id,
            'packing_cost': item.variant.product.packing_cost,
            'tax': item.variant.product.tax,
            'model_name': item.variant.product.model_name,
            'brand_name': item.variant.product.brand.Brand_name if item.variant.product.brand else '',
            'tag_name': item.variant.product.Tags.name if item.variant.product.Tags else '',
            'quantity': item.quantity,
            # Add more fields as needed
        })
    cart_products_ids = [item['id'] for item in cart_products]
    cart_products_ids_list = [int(id) for id in cart_products_ids]

    
    # for item in cart.items.all():
    #     cart_products.append(item.variant)

    context = {
        'product': product,
        'comments': comments,
        'avg_rating': avg_rating,
        'user_rating': user_rating,
        'cart_products': cart_products,
        'variants': variants,  # Changed to 'variants' instead of 'variant'
        'product_variant': product_variant,
        'variant_images': variant_images,
        'cart_products_ids_list':cart_products_ids_list,
    }

    # Fetch unique colors and sizes for variant selection
    unique_colors = variants.values_list('color__name', flat=True).distinct()
    unique_sizes = variants.values_list('size__name', flat=True).distinct()
    color_radio = variant.color.name
    size_radio = variant.size.name
    context.update({
        'unique_colors': unique_colors,
        'unique_sizes': unique_sizes,
        "color_radio":color_radio,
        "size_radio":size_radio,
    })

    if request.method == 'POST':
        v_color = request.POST.get('color')
        v_size = request.POST.get('size')
        if v_color and v_size is not None:
            color_filter = variants.filter(size__name=v_size)
            selected_variants_or = variants.filter(Q(color__name=v_color) | Q(size__name=v_size))
            selected_variants_and = variants.filter(Q(color__name=v_color) & Q(size__name=v_size))
            unique_colors = []
            for i in color_filter:
                unique_colors.append(i.color)
            color_radio = v_color if v_color else unique_colors[0].name if unique_colors else ''
            size_radio = v_size if v_size else unique_sizes[0] if unique_sizes else ''
            context.update({
                "color_radio": color_radio,
                "size_radio": size_radio
            })
        else:
            selected_variants_and = Variants.objects.filter(product=product)
            size_radio = unique_sizes[0] if unique_sizes else ''
            color_radio = unique_colors[0] if unique_colors else ''


            context.update({
                "color_radio": color_radio,
                "size_radio": size_radio
            })

        if selected_variants_and.exists():
            selected_variant = selected_variants_and.first()
        else:
            selected_variant = selected_variants_or.first()

        variant_details = {
            'id': selected_variant.id if selected_variant else None,
            'name': selected_variant.title if selected_variant else '',
            'color': selected_variant.color.name if selected_variant and selected_variant.color else '',
            'size': selected_variant.size.name if selected_variant and selected_variant.size else '',
            'price': selected_variant.price if selected_variant else 0,
            'image_url': selected_variant.image_id.url if selected_variant and selected_variant.image_id else '',
        }
        variant_images = Variant_image.objects.filter(variant=variant_details['id'])
        product_variant = variant_details
        context.update({
            'product_variant': product_variant,
            "variant_images": variant_images,
            'unique_colors': unique_colors,
        })
    main_category, category, Sub_category = categories_function(request)

    context.update({
        "main_category":main_category,
        "category":category,
        "Sub_category":Sub_category
    })
    scroll_position = request.GET.get('scroll_position', 0)
    context['scroll_position'] = scroll_position
    return render(request, 'Main/product_detail.html', context=context)




def update_colors(request):
    size = request.GET.get('size')
    # Your logic to get colors based on the selected size
    colors = Color.objects.filter(variant__size=size).distinct()
    colors_html = ''.join([f'<label>{color.name}<input type="radio" name="color" value="{color.name}"></label>' for color in colors])
    return JsonResponse({'colors_html': colors_html})

def update_variants(request):
    size = request.GET.get('size')
    color = request.GET.get('color')
    # Your logic to get variants based on the selected size and color
    variants = Variants.objects.filter(size=size, color__name=color)
    variants_html = ''.join([f'<div>{variant.name}</div>' for variant in variants])
    return JsonResponse({'variants_html': variants_html})


def get_colors(request):
    size = request.GET.get('size')
    # Query your database to get colors based on the selected size
    colors = Variants.objects.filter(size__name=size).values('color__id', 'color__name')
    return JsonResponse({'colors': list(colors)})


def get_variant_details(request):
    if request.method == 'GET':
        variant_id = request.GET.get('variant_id')
        try:
            variant = Variants.objects.get(id=variant_id)
            data = {
                'price': variant.price,
                'image_url': variant.image().url if variant.image() else '',
            }
            return JsonResponse(data)
        except Variants.DoesNotExist:
            return JsonResponse({'error': 'Variant not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def error_handler(request, status_code=None, exception=None):
    return render(request, 'error.html', {'status_code': status_code, 'exception': exception}, status=status_code)

def add_comment(request, slug):
    product = get_object_or_404(Product, slug=slug)
    user = request.user
    content = request.POST.get('content')
    numeric_rating = int(request.POST.get('numeric_rating', 0))
    image = request.FILES.get('image', None)

    Comment.objects.create(product=product, user=user, content=content, numeric_rating=numeric_rating, image=image)

    return JsonResponse({'status': 'success'})


def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login/')
    else:
        data = ({"amount": 500,
                 "currency": "INR",
                'payment_capture': '1',
                 })
        payment = client.order.create(data=data)

        order_id = payment['id']
        
        cart = request.session.get('cart')
        packing_cost = sum(i['packing_cost'] for i in cart.values() if i)
        tax = 0
        for i in cart.values():
            c = i['price'] * i['tax'] / 100
            tax += c
        coupon = None
        valid_coupon = None
        invalid_coupon = None
        if request.method == 'GET':
            coupon_code = request.GET.get('c')
            if coupon_code:
                try:
                    coupon = Coupon.objects.get(code=coupon_code)
                    valid_coupon = "Is a valid coupon code"

                except:
                    invalid_coupon = "Invalid coupon code"
        user = User.objects.all().first()
        

        params = {
            'packing_cost': packing_cost,
            'tax': tax,
            'coupon': coupon,
            'valid_coupon': valid_coupon,
            'invalid_coupon': invalid_coupon,
            'order_id': order_id,
            'payment': payment,
            'user':user
        }
        return render(request, 'Main/checkout.html', params)


def Placeorder(request):
    if request.method == "POST":
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id=uid)
        ordered_product= request.POST.get('all_products')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('Email')
        # state = request.POST.get('State')
        city = request.POST.get('City')
        zip_code = request.POST.get('Zip-Code')
        additional_info = request.POST.get('Add_Info')
        address = request.POST.get('Address')
        phone = request.POST.get('phone')
        amount=request.POST.get('amount')
        order_id = request.POST.get('order_id')
        payment=request.POST.get('payment')
        # prnt(firstname,lastname,email,city,zip_code,additional_info,address,phone,amount,order_id,payment)
       
        order = Order(
            user=user,
            ordered_product=ordered_product,
            firstname=firstname,
            lastname=lastname,
            email=email,
            address=address,
            city=city,
            # state=state,
            zip_code=zip_code,
            additional_info=additional_info,
            phone=phone,
            payment_id=order_id,
            amount=amount,
        )
        order.save()
        return render(request, 'Main/place_order.html')

def My_Account(request):
    # return render(request,'../templates/Error_pages/404.html')

    return render(request,'../templates/Account/My_account.html')


def handle_404(request):
    return render(request,'../templates/Error_pages/404.html',{})

def handle_404_error(request,exception):
    return render(request,'../templates/Error_pages/404.html',status=404)

def handle_400_error(request,exception):
    return render(request,'../templates/Error_pages/404.html',status=400)

def handle_403_error(request,exception):
    return render(request,'../templates/Error_pages/404.html',status=403)

def handle_500_error(request,exception=None):
    return render(request,'../templates/Error_pages/404.html',{})

