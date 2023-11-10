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
    main_category = Main_categorie.objects.all().order_by()
    category = Categorie.objects.all().order_by('-id')
    Sub_category = Sub_categorie.objects.all().order_by('-id')
    # products = Product.objects.filter(Section__name = 'New Arival')
    partners = Partners.objects.all().order_by('-id')
    products = Product.objects.all()
    # most_selling_products = Product.objects.annotate(quantity_sold=F('total_quantity') - F('Availability')).order_by('-quantity_sold')[:6]
    most_selling_products = Product.objects.annotate(quantity_sold=F('total_quantity') - F('Availability')).order_by('-quantity_sold')[:10]
    home_and_kitchen = Product.objects.filter(Section__name="Home & Kitchen")
    top_featured_product = Product.objects.filter(Section__name="Top Featured Product")
    top_featured_product_4 = Product.objects.filter(Section__name="Top Featured Product")[1:5]
    top_discount_products = Product.objects.order_by('-Discount')[:10]
    

    cart = Cart(request)
    cart_products = []
    for item in cart.cart:
        cart_products.append(int(item))


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


# def product_detail(request, slug):
#     product = Product.objects.get(slug=slug)
#     comments = Comment.objects.filter(product=product)
#     likes = Like.objects.filter(product=product)

#     context = {
#         'product': product,
#         'comments': comments,
#         'likes': likes,
#     }
#     return render(request, 'product_detail.html', context)

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

    
    params['category']=category
    params['subcategory']=subcategory
    params['cart_products']=cart_products
    params['current_page']=current_page,

    
    return render(request,'../templates/Main/shop.html',context=params)



def filter_products(request):
    if request.method == 'POST':
        # Get filter parameters from the form
        min_price = request.POST.get('min_price', 0)
        max_price = request.POST.get('max_price', float('inf'))
        selected_colors_list = request.POST.getlist('color')
        selected_sizes_list = request.POST.getlist('size')
        selected_brands_list = request.POST.getlist('brands')

        # Convert the received values to integers
        selected_colors = [int(color_id) for color_id in selected_colors_list]
        selected_sizes = [int(size_id) for size_id in selected_sizes_list]
        selected_brands = [int(brand_id) for brand_id in selected_brands_list]

        # Filter products based on selected options
        products = Product.objects.filter(
            price__range=(min_price, max_price),
            color__in=selected_colors if selected_colors else Color.objects.values_list('id', flat=True),
            size__in=selected_sizes if selected_sizes else Size.objects.values_list('id', flat=True),
            brand__id__in=selected_brands if selected_brands else Brands.objects.values_list('id', flat=True),
        )

        # Render the template with the filtered products
        return render(request, 'Main/shop.html', {'products': products})

    # Handle GET request, render the initial form
    return render(request, 'Main/shop.html', {})


def add_to_cart(request):
    if request.method == 'POST':
        # Your logic to determine the product or variant to add to the cart
        # ...

        # For example, adding a product with id
        product_id = request.POST.get('product_id')
        quantity = 1

        # Use the cart_add view to add the product to the cart
        response = cart_add(request, product_id, quantity)

        # You can customize the response as needed
        if response.get('status') == 'success':
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Error adding to cart'})

    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


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
    # print(CATID)
    SUBCATID=request.GET.get('sub_category')

    # print(category_id)
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
            Q(name__icontains=term) |
            Q(Category__name__icontains=term) |
            Q(Sub_category__name__icontains=term) |
            Q(brand__Brand_name__icontains=term) |
            Q(Tags__name__icontains=term) |
            Q(size__name__icontains=term) |
            Q(color__code__icontains=term) |
            (Q(price__lte=float(term)) if is_valid_number(term) else Q()) |
            (Q(Discount__gte=float(term)) if is_valid_number(term) else Q())
        )


    # Use the Q object in the filter to get relevant products
    products = Product.objects.filter(q_objects)

    related_categories = products.values_list('Category__name', flat=True).distinct()
    related_subcategories = products.values_list('Sub_category__name', flat=True).distinct()
    related_brands = products.values_list('brand__Brand_name', flat=True).distinct()
    related_tags = products.values_list('Tags__name', flat=True).distinct()
    related_size = products.values_list('size__name', flat=True).distinct()
    related_colors = products.values_list('color__code', flat=True).distinct()

    # print(related_brands,related_categories,related_subcategories,related_tags,related_colors,related_size)
    params = {
        'products': products,
        'related_categories': related_categories,
        'related_subcategories': related_subcategories,
        'related_brands': related_brands,
        'related_colors':related_colors,
        'related_size':related_size,
    }
    
    
    return render(request,'../templates/Main/search.html',context=params)



def PRODUCT_DETAIL(request, slug):
    product = get_object_or_404(Product, slug=slug)
    comments = Comment.objects.filter(product=product)
    avg_rating = comments.aggregate(avg_rating=models.Avg('numeric_rating'))['avg_rating']
    user_rating = None  # You can implement this based on user authentication
    cart = Cart(request)
    cart_products = [int(item) for item in cart.cart]

    variants = Variants.objects.filter(product=product)
    
    selected_details = {
    'name': product.name,
    'color': product.color.name if product.color else '',
    'size': product.size.name if product.size else '',
    'price': product.price,
    'image_url': product.image.url if product.image else '',
    'product_image': product.product_image_set.all(),
}
    
    
    # Fetch all variant details for each variant
    variant_details = [
        {
            'id': variant.id,
            'title': variant.title,
            'color_name': variant.color.name if variant.color else '',
            'size': variant.size.name if variant.size else '',
            'price': variant.price,
            'image_url': variant.image().url if variant.image_id else '',
        }
        for variant in variants
    ]
    
    context = {
        'product': product,
        'comments': comments,
        'avg_rating': avg_rating,
        'user_rating': user_rating,
        'cart_products': cart_products,
        'variants': variants,
        'variant_details': variant_details,
        'selected_details': selected_details,
    }

    if variants.exists():
        # Fetch unique colors and sizes for variant selection
        unique_colors = variants.values_list('color__name', flat=True).distinct()
        unique_sizes = variants.values_list('size__name', flat=True).distinct()
        context.update({
            'unique_colors': unique_colors,
            'unique_sizes': unique_sizes,
        })

    if request.method == 'GET':
        v_color = request.GET.get('color')
        v_size = request.GET.get('size')
        selected_variants = variants.filter(Q(color__name=v_color) | Q(size__name=v_size))

        if selected_variants.exists():
                selected_variant = selected_variants.first()  # You might need to adjust this based on your logic
                
                # Extract specific details for the selected variant
                selected_details = {
                    'id':selected_variant.id,
                    'name': selected_variant.title,
                    'color': selected_variant.color.name if selected_variant.color else '',
                    'size': selected_variant.size.name if selected_variant.size else '',
                    'price': selected_variant.price,
                    'image_url': selected_variant.image().url if selected_variant.image_id else '',
                }

                # Include the selected details in the context
                context.update({'selected_details': selected_details})

    scroll_position = request.GET.get('scroll_position', 0)

    # Include the scroll position in the context
    context['scroll_position'] = scroll_position   
    return render(request, 'Main/product_detail.html', context)

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

