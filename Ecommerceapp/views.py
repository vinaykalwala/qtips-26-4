import os
from django.http import HttpResponseRedirect, JsonResponse,HttpResponse
from math import ceil
from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from flask import Response
from Ecommerceapp.models import *
from django.db.models import Q
from itertools import groupby,chain
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
from django.views.decorators.cache import cache_page


# from cart.cart import Cart
from django.db.models import Count
from django.db.models import Q, Count, Case, When, Value, IntegerField
import razorpay
from .forms import *
from django.db.models import Min,Max,Sum
# from ..CART.models import
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
client=razorpay.Client(auth=("rzp_test_T93mYNB9ALYhh9", "hUnFTkG7Crc0futErJopKuae"))



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
    user = request.user

    if user.is_authenticated:
        try:
            user_carts = User_Cart.objects.filter(user=user)

            if user_carts.exists():
                # Choose a specific cart based on your logic
                user_cart = user_carts.first()
            else:
                # Handle the case when no cart is found
                logger.error(f"No User_Cart found for user ID: {user.id}")
                user_cart = None

        except User_Cart.DoesNotExist:
            logger.error(f"No User_Cart found for user ID: {user.id}")
            user_cart = None
    else:
        # Handle the case when the user is not authenticated
        user_cart = None

    # print(user_cart.cart_items)

    cart_products = []
    cart_products_ids_list = []
    cart_count=0

    if user_cart:
        cart_items = user_cart.cart_items.all()

        for item in cart_items:
            cart_products.append({
                'id': item.variant.id,
                'variant_title': item.variant.title,
                'variant_price': item.variant.price,
                'variant_image_url': item.variant.image_id if item.variant.image_id else '',
                'variant_size': item.variant.size.name if item.variant.size else '',
                'variant_color': item.variant.color.name if item.variant.color else '',
                'product_id': item.variant.product.id,
                'product_slug': item.variant.product.slug,
                'packing_cost': item.variant.product.packing_cost,
                'tax': item.variant.product.tax,
                'model_name': item.variant.product.model_name,
                'brand_name': item.variant.product.brand.Brand_name if item.variant.product.brand else '',
                'tag_name': item.variant.product.Tags.name if item.variant.product.Tags else '',
                'quantity': item.quantity,
                # Add more fields as needed
            })
            cart_products_ids_list.append(item.variant.id)
            cart_count = len(cart_products_ids_list)

    return cart_products,cart_products_ids_list,cart_count

def categories_function(request):
    main_category = Main_categorie.objects.all().order_by()
    category = Categorie.objects.all().order_by('-id')
    Sub_category = Sub_categorie.objects.all().order_by('-id')

    return main_category,category,Sub_category

def privacy_policy(request):
    main_category, category, sub_category = categories_function(request)
    cart_products, cart_products_ids_list, cart_count = cart_function(request)
    params={
        'cart_products': cart_products,
        'cart_count': cart_count,
        'cart_products_ids_list': cart_products_ids_list,
        'main_category': main_category,
        'category': category,
        'sub_category': sub_category,
        }
    return render(request,'../templates/Main/privacy_policy.html',context=params)
def shipping_policy(request):
    main_category, category, sub_category = categories_function(request)
    cart_products, cart_products_ids_list, cart_count = cart_function(request)
    params={
        'cart_products': cart_products,
        'cart_count': cart_count,
        'cart_products_ids_list': cart_products_ids_list,
        'main_category': main_category,
        'category': category,
        'sub_category': sub_category,
        }
    return render(request,'../templates/Main/shipping_policy.html',context=params)
def payment_policy(request):
    main_category, category, sub_category = categories_function(request)
    cart_products, cart_products_ids_list, cart_count = cart_function(request)
    params={
        'cart_products': cart_products,
        'cart_count': cart_count,
        'cart_products_ids_list': cart_products_ids_list,
        'main_category': main_category,
        'category': category,
        'sub_category': sub_category,
        }
    return render(request,'../templates/Main/payment_policy.html',context=params)
def return_refund(request):
    main_category, category, sub_category = categories_function(request)
    cart_products, cart_products_ids_list, cart_count = cart_function(request)
    params={
        'main_category': main_category,
        'category': category,
        'sub_category': sub_category,
        'cart_products': cart_products,
        'cart_count': cart_count,
        'cart_products_ids_list': cart_products_ids_list,
        }
    return render(request,'../templates/Main/return_refund.html',context=params)

from django.db.models import F
from django.views.decorators.cache import cache_page

def product_deals(request,slug,deal_id,banner_id):
    discount_deal = get_object_or_404(Discount_deal, slug=slug, id=deal_id)
    banner=Banners.objects.get(id=banner_id)
    # Retrieve the related products for the given discount_deal
    discount = 0  # Set the default discount to 0

    products = Product.objects.filter(Deals=discount_deal)
    # Check if the product has an associated deal in Banners
    modified_products = []

    for product in products:
        discount = 0  # Set the default discount to 0

        # Check if the product has an associated deal in Banners
        if product.Deals:
            # Get the associated discount from the Banners model
            discount = product.Deals.Discount
            viewed.objects.create(user=request.user, product=product)

        # Update the price of the product in the dictionary
        modified_product = {
            'image': get_image_url(product),
            'id': product.id,
            'slug': product.slug,
            'name': product.name,
            'total_quantity': product.total_quantity,
            'Availability': product.Availability,
            'price':product.price,
            'discounted_price': product.price - (product.price * discount) / 100,  # Change the price according to the discount
            'Product_info': product.Product_info,
            'Description': product.Description,
        }
    viewed.objects.create(user=request.user, product=product)
    
    context = {
        'discount_deal': discount_deal,
        'products': modified_products,
        'banner':banner,
        
    }
    return render(request,'Main/deals_product.html',context=context)

def get_image_url(product):
    if product.image:
        local_path = os.path.join('media', str(product.image))
        if os.path.exists(local_path):
            print(f'/media/{product.image}')
            return f'/media/{product.image}'
        else:
            # Replace this with the actual AWS S3 URL retrieval logic
            return product.image.url
    else:
        return ''
    


def get_products_by_section(section_list, max_products=10):
    products_list = []

    for section in section_list:
        # Using select_related to fetch related Section data in a single query
        products = Product.objects.filter(Section=section).select_related('Section')[:max_products]

        section_data = {
            'name': section.name,
            'products': [
                {
                    'image': product.image,
                    'id': product.id,
                    'slug': product.slug,
                    'name': product.name,
                    'total_quantity': product.total_quantity,
                    'availability': product.Availability,
                    'price': product.price,
                    'product_info': product.Product_info,
                    'description': product.Description,
                    'discount': product.Discount,
                    'rating': product.rating,
                }
                for product in products
            ]
        }
        products_list.append(section_data)

    return products_list
from django.shortcuts import render
from django.utils import timezone
from .models import Sliders, Banners, Section, Product, Deal_of_the_day, Top_Featured, Moving_text, Categorie


def index(request):
    current_page = 'home'

    # Fetch banners
    slider_imgs = Sliders.objects.all().order_by('-id')
    banner_1 = Banners.objects.filter(section__name="HTB_L").order_by('-id')
    banner_2 = Banners.objects.filter(section__name="HTB_R").order_by('-id')[:4]
    banner_3 = Banners.objects.filter(section__name="HBB").order_by('-id')[:6]

    # Fetch sliders
    sliders = Sliders.objects.all()

    # Fetch categories using a separate function
    main_category, category, sub_category = categories_function(request)

    # Fetch top featured products
    top_Featured_L = Top_Featured.objects.first()
    if top_Featured_L:
        top_Featured_R = Top_Featured.objects.exclude(pk=top_Featured_L.pk)[:4]
    else:
        top_Featured_R = []

    # Fetch sections with products
    sections = Section.objects.filter(contains_products=True)
    section_1 = sections[:4][::-1]
    products_list_1 = get_products_by_section(section_1)
    section_2 = sections[4:8][::-1]
    products_list_2 = get_products_by_section(section_2)

    # Fetch recently added products
    recently_added_products = Product.objects.order_by('-id')[:10]

    # Fetch deal of the day and top deals of the day
    deal = Deal_of_the_day.objects.first()
    topDealsOfTheDay = Deal_of_the_day.objects.all()[:2]

 

    # Initialize countdown_datetime
    countdown_datetime = None

    # Calculate countdown_datetime if deal exists and has end time
    if deal and deal.deal_end_time and deal.deal_end_time > timezone.now():
        countdown_datetime = deal.deal_end_time.isoformat()


    # Fetch cart information using a separate function
    popular_categories = Categorie.objects.filter(popular=True)
    cart_products, cart_products_ids_list, cart_count = cart_function(request)

    # Fetch moving text for home section
    moveing_text = Moving_text.objects.filter(section__name='Home')

    # Prepare context dictionary
    context = {
        'slider_imgs': slider_imgs,
        'countdown_datetime': countdown_datetime,
        'main_category': main_category,
        'category': category,
        'sub_category': sub_category,
        'products_list_1': products_list_1,
        'products_list_2': products_list_2,
        'moveing_text': moveing_text,
        'sliders': sliders,
        'top_Featured_R': top_Featured_R,
        'top_Featured_L': top_Featured_L,
        'topDealsOfTheDay': topDealsOfTheDay,
        'recently_added_products': recently_added_products,
        'banner_1': banner_1,
        'banner_2': banner_2,
        'banner_3': banner_3,
        'cart_products': cart_products,
        'cart_count': cart_count,
        'cart_products_ids_list': cart_products_ids_list,
        'current_page': current_page,
        'popular_categories': popular_categories,
    }

    return render(request, 'Main/index.html', context)

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
    product.update_average_rating()
    return JsonResponse({'status': 'success'})

from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import Contact
from django.views.decorators.csrf import csrf_exempt



# myapp/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Contact
import json

@csrf_exempt
def contact(request):
    print(f"Request method: {request.method}")  # Debug: Print request method
    
    if request.method == 'POST':
        # Try to parse POST data from request.body
        try:
            data = json.loads(request.body)
            email = data.get('email')
            name = data.get('name')
            subject = data.get('subject')
            message = data.get('message')
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
        
        print(f"Email: {email}, Name: {name}, Subject: {subject}, Message: {message}")  # Debug: Print extracted data
        
        # Check if all required data is present
        if email and name and subject and message:
            # Create and save Contact object
            contact = Contact(email=email, name=name, subject=subject, message=message)
            contact.save()
            return JsonResponse({'success': True, 'message': 'Contact saved successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Missing form data'}, status=400)
    else:
          return render(request, 'Main/contact.html')





def ABOUT(request):
    current_page = 'about'
    cart_products,cart_products_ids_list,cart_count = cart_function(request)
    main_category, category, sub_category = categories_function(request)

    params = {
        'cart_products': cart_products,
        'cart_count':cart_count,
        'cart_products_ids_list':cart_products_ids_list,
                'current_page':current_page,
                'main_category': main_category,
        'category': category,
        'sub_category': sub_category,

    }

    return render(request,'../templates/Main/about.html',context=params)



from django.db.models import Q
from django.db.models import Q
from decimal import Decimal

def PRODUCTS(request, sub_category_):
    sub_category_ = get_object_or_404(Sub_categorie, id=sub_category_)
    

    # Retrieve unique brands, colors, and sizes
    unique_brands = Product.objects.filter(Sub_category=sub_category_).values('brand__Brand_name').annotate(count=Count('brand__Brand_name'))
    unique_colors = Variants.objects.filter(product__Sub_category=sub_category_, color__isnull=False).values('color__name').annotate(count=Count('color__name'))
    unique_sizes = Variants.objects.filter(product__Sub_category=sub_category_, size__isnull=False).values('size__name').annotate(count=Count('size__name'))

    # Define price ranges
    price_ranges = [
        {"label": "Under ₹500", "min": Decimal("0.00"), "max": Decimal("500.00")},
        {"label": "₹500 - ₹1000", "min": Decimal("500.00"), "max": Decimal("1000.00")},
        {"label": "₹1000 - ₹5000", "min": Decimal("1000.00"), "max": Decimal("5000.00")},
        {"label": "Over ₹5000", "min": Decimal("5000.00"), "max": Decimal("1000000.00")},  # Adjust upper limit as needed
    ]

    # Apply the filters
    selected_colors = request.GET.getlist('color')
    selected_brands = request.GET.getlist('brand')
    selected_sizes = request.GET.getlist('size')
    selected_prices = request.GET.getlist('price')
    selected_discount = request.GET.get('discount')
    selected_rating_range = request.GET.get('rating')

    color_conditions = Q()
    brand_conditions = Q()
    size_conditions = Q()
    price_conditions = Q()
    discount_conditions = Q()
    rating_conditions = Q()

    if selected_colors:
        color_conditions |= Q(variants__color__name__in=selected_colors)

    if selected_brands:
        brand_conditions |= Q(brand__Brand_name__in=selected_brands)

    if selected_sizes:
        size_conditions |= Q(variants__size__name__in=selected_sizes)

    for price_range in price_ranges:
        if price_range['label'] in selected_prices:
            price_conditions |= Q(price__range=(price_range['min'], price_range['max']))

    if selected_discount:
        discount_conditions |= Q(Discount__gte=int(selected_discount.split('-')[0]))

    if selected_rating_range:
        min_rating, max_rating = map(int, selected_rating_range.split('-'))
        rating_conditions |= Q(rating__range=(min_rating, max_rating))

    # Initial retrieval of products based on the sub-category
    products = Product.objects.filter(Sub_category=sub_category_)

    # Apply filters to get filtered products
    filtered_products = products.filter(color_conditions | brand_conditions | size_conditions | price_conditions | discount_conditions | rating_conditions).distinct() 

    # Pagination for products based on the sub-category
    page = request.GET.get('page', 1)
    items_per_page = 10
    paginator = Paginator(filtered_products, items_per_page)

    try:
        products_paginated = paginator.page(page)
    except PageNotAnInteger:
        products_paginated = paginator.page(1)
    except EmptyPage:
        products_paginated = paginator.page(paginator.num_pages)

    # Create a dictionary with all the parameters for products
    cart_products, cart_products_ids_list, cart_count = cart_function(request)
    main_category, category, sub_category = categories_function(request)

    params = {
        'products': products_paginated,
        'sub_category': sub_category,
        'unique_brands': unique_brands,
        'unique_colors': unique_colors,
        'unique_sizes': unique_sizes,
        'price_ranges': price_ranges,
        'selected_colors': selected_colors,
        'selected_brands': selected_brands,
        'selected_sizes': selected_sizes,
        'selected_prices': selected_prices,
        'selected_discount': selected_discount,
        'selected_rating_range': selected_rating_range,
        'cart_products': cart_products,
        'cart_count': cart_count,
        'cart_products_ids_list': cart_products_ids_list,
        'main_category': main_category,
        'category': category,
        'sub_category': sub_category,
        'sub_category_': sub_category_,
    }

    return render(request, 'Main/shop.html', context=params)


def CATS(request):
    current_page = 'shop'

    brands = Brands.objects.all()
    products = Product.objects.all()
    main_category = Main_categorie.objects.all()
    category = Categorie.objects.all()
    sub_category = Sub_categorie.objects.all()

    CATID = request.GET.get('categories')
    MAIN_CATID = request.GET.get('main_categories')
    BRAND_ID = request.GET.get('brands')
    main_category, category, sub_category = categories_function(request)
    Header_icons = Header_Icons.objects.all()[:7]

    if CATID:
        sub_category = Sub_categorie.objects.filter(Category=CATID)

    if BRAND_ID:
        products = Product.objects.filter(brand=BRAND_ID)
    if MAIN_CATID:
        category = Categorie.objects.filter(main_category=MAIN_CATID)

    # Pagination
    page = request.GET.get('page', 1)
    items_per_page = 10  # Adjust this value as needed
    paginator = Paginator(products, items_per_page)

    try:
        products_paginated = paginator.page(page)
    except PageNotAnInteger:
        products_paginated = paginator.page(1)
    except EmptyPage:
        products_paginated = paginator.page(paginator.num_pages)

    cart_products,cart_products_ids_list,cart_count = cart_function(request)


    params = {
        'products': products_paginated,
        'category': category,
        'brands': brands,
        'sub_category': sub_category,
        'main_category': main_category,
        "Header_icons": Header_icons,
        'current_page': current_page,
        'cart_products': cart_products,
        'cart_count':cart_count,
        'cart_products_ids_list':cart_products_ids_list,
        'main_category': main_category,
        'category': category,
        'sub_category': sub_category,

    }

    return render(request, '../templates/Main/cats.html', context=params)



def SUBCATS(request):
    current_page = 'shop'
    main_category, category, sub_category = categories_function(request)

    brands = Brands.objects.all()
    products = Product.objects.all()
    category_ = Categorie.objects.all()[:1]
    CATID = request.GET.get('categories')
    SUBCATID = request.GET.get('sub_category')

    Header_icons = Header_Icons.objects.all()[:7]
    BRAND_ID = request.GET.get('brands')

    if CATID:
        products = Product.objects.filter(Category=CATID)
        sub_category_ = Sub_categorie.objects.filter(category=CATID)
    if BRAND_ID:
        products = Product.objects.filter(brand=BRAND_ID)
        sub_category_ = Sub_categorie.objects.filter(category=CATID)
    if SUBCATID:
        products = Product.objects.filter(Sub_category=SUBCATID)
        sub_category_ = Sub_categorie.objects.filter(category=CATID)

    # Group variants by color
    products_with_colors = []
    for product in products:
        variants = Variants.objects.filter(product=product)
        unique_colors = set(variant.color.code for variant in variants if variant.color)
        products_with_colors.append({'product': product, 'colors': unique_colors})

    # Pagination
    page = request.GET.get('page', 1)
    items_per_page = 10  # Adjust this value as needed
    paginator = Paginator(products, items_per_page)

    try:
        products_paginated = paginator.page(page)
    except PageNotAnInteger:
        products_paginated = paginator.page(1)
    except EmptyPage:
        products_paginated = paginator.page(paginator.num_pages)


    cart_products,cart_products_ids_list,cart_count = cart_function(request)


    params = {
        'products': products_paginated,
        'category': category,
        'brands': brands,
        'sub_category_': sub_category_,
        'Header_icons': Header_icons,
        'current_page': current_page,
        'products_with_colors': products_with_colors,
        'cart_products': cart_products,
        'cart_count':cart_count,
        'cart_products_ids_list':cart_products_ids_list,
        'main_category': main_category,
        'category': category,
        'sub_category': sub_category,

    }

    return render(request, '../templates/Main/sub_cats.html', context=params)





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

def calculate_variant_total(variant_id):
    variant = get_object_or_404(Variants, id=variant_id)
    return variant.price

@login_required(login_url="/auth/login")
def cart_detail(request):
    cart_products, cart_products_ids_list, cart_count = cart_function(request)

    packing_cost = 0
    tax = 0

    for item in cart_products:
        if 'packing_cost' in item and item['packing_cost'] is not None:
            packing_cost += item['packing_cost']

        if 'variant_price' in item and 'tax' in item and item['variant_price'] is not None and item['tax'] is not None:
            tax += (item['variant_price'] * item['tax']) / 100

    coupon = None
    valid_coupon = None
    invalid_coupon = None

    if request.method == 'GET':
        coupon_code = request.GET.get('coupon_code')

        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                valid_coupon = "Is a valid coupon code"
            except Coupon.DoesNotExist:
                invalid_coupon = "Invalid coupon code"
    subtotals = 0
    for value in cart_products:
        variant_total = calculate_variant_total(value['id'])  # Assuming you have a function to calculate variant total
        subtotals += value['quantity'] * variant_total

    total_amount = subtotals + tax + packing_cost + 70

    if valid_coupon:
        coupon_discount = (subtotals * coupon.discount) / 100
        total_amount -= coupon_discount

    context = {
        'subtotals': subtotals,
        'cart_products': cart_products,
        'cart_count': cart_count,
        'packing_cost': packing_cost,
        'tax': tax,
        'coupon': coupon,
        'valid_coupon': valid_coupon,
        'invalid_coupon': invalid_coupon,
        'total_amount':total_amount,
    }

    return render(request, 'cart/cart_detail.html', context)

def is_valid_number(term):
    try:
        float(term)
        return True
    except ValueError:
        return False
  # Import the form you need

def Search(request):
    present_search_query = getattr(request, 'search_query', '')
    searched_query = present_search_query or request.GET.get('query_pass', '')
    main_category, category, sub_category = categories_function(request)


    search_terms = searched_query.split()

    q_objects_search = Q()
    for term in search_terms:
        q_objects_search |= (
            Q(variants__title__icontains=term) |
            Q(variants__color__name__icontains=term) |
            Q(variants__size__name__icontains=term) |
            Q(Category__name__icontains=term) |
            Q(Sub_category__name__icontains=term) |
            Q(brand__Brand_name__icontains=term) |
            Q(Tags__name__icontains=term) |
            (Q(price__lte=float(term)) if is_valid_number(term) else Q()) |
            (Q(Discount__gte=float(term)) if is_valid_number(term) else Q())
        )

    variants_search = Product.objects.filter(q_objects_search).distinct()

    # brand = request.GET.getlist('brand', [])
    # color = request.GET.getlist('color', [])
    # size = request.GET.getlist('size', [])
    # min_price = request.GET.get('min_price')
    # max_price = request.GET.get('max_price')

    q_objects_filter = Q()

    # if brand:
    #     q_objects_filter |= Q(product__brand__Brand_name__in=brand)

    # if color:
    #     q_objects_filter |= Q(color__name__in=color)

    # if size:
    #     q_objects_filter |= Q(size__name__in=size)

    # if min_price:
    #     q_objects_filter |= Q(product__price__gte=min_price)

    # if max_price:
    #     q_objects_filter |= Q(product__price__lte=max_price)

    variants_filter = variants_search.filter(q_objects_filter).distinct()


    # cart = Cart(request)
    cart_products, cart_products_ids_list,cart_count = cart_function(request)
    # cart_products = [item.variant_id for item in cart.cart]

    for variant in variants_filter:
        variant.in_cart = variant.id in cart_products

    page_number = request.GET.get('page', 1)
    items_per_page = 20
    print(variants_filter)
    paginator = Paginator(variants_filter, items_per_page)

    try:
        paginated_variants = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_variants = paginator.page(1)
    except EmptyPage:
        paginated_variants = paginator.page(paginator.num_pages)


    unique_colors = Product.objects.filter(q_objects_search).values('variants__color__name').distinct()
    unique_brands = Product.objects.filter(q_objects_search).values('brand__Brand_name').distinct()
    unique_sizes = Product.objects.filter(q_objects_search).values('variants__size__name').distinct()

    selected_colors = request.GET.getlist('color')
    selected_brands = request.GET.getlist('brand')
    selected_sizes = request.GET.getlist('size')
    # print(paginated_variants[0])

    params = {
        'variants': paginated_variants,
        'cart_products_ids_list': cart_products_ids_list,
        'cart_products': cart_products,
        'cart_count':cart_count,
        'searched_query': searched_query,
        'unique_colors': unique_colors,
        'unique_brands': unique_brands,
        'unique_sizes': unique_sizes,
        'selected_colors': selected_colors,
        'selected_brands': selected_brands,
        'selected_sizes': selected_sizes,
        'sub_category':sub_category,
        'category':category,
        'main_category':main_category,

    }

    return render(request, 'Main/search.html', context=params)



import logging

logger = logging.getLogger(__name__)


def get_variant_details(selected_variant):
    return {
        'id': selected_variant.id if selected_variant else None,
        'title': selected_variant.title if selected_variant else '',
        'color': selected_variant.color.name if selected_variant and selected_variant.color else '',
        'size': selected_variant.size.name if selected_variant and selected_variant.size else '',
        'price': selected_variant.price if selected_variant else 0,
        'image_url': selected_variant.image_id if selected_variant and selected_variant.image_id else '',
    }

import json
from django.core.serializers.json import DjangoJSONEncoder
logger = logging.getLogger(__name__)
from datetime import datetime, timedelta


def calculate_delivery_date(pincode):
    # Assume some logic to determine distance based on pincode
    distance = get_distance_from_location(pincode)

    # Determine estimated delivery date based on distance
    if distance <= 10:
        delivery_days = 3  # Delivery in 3 days for locations within 10 km
    else:
        delivery_days = 4  # Delivery in 4 days for locations beyond 10 km

    # Calculate delivery date by adding delivery days to current date
    delivery_date = datetime.now() + timedelta(days=delivery_days)

    return delivery_date.strftime("%Y-%m-%d")  # Format delivery date as string

def get_distance_from_location(pincode):
    # This is a placeholder function to simulate distance calculation
    # Replace it with your actual logic to determine distance based on pincode
    # For simplicity, we'll just return a constant distance for demonstration
    return 10  # Assume a constant distance of 10 km for demonstration
    
    
    
    from django import forms

class PincodeForm(forms.Form):
    pincode = forms.CharField(max_length=10)  # Adjust the max_length as needed

    
    
    
    from django.db.models import Q
    import datetime


def prod_detail(request, slug, product_id=None, variant_id=None, color=None, size=None):
    try:
        product = Product.objects.get(slug=slug)
    except Product.MultipleObjectsReturned:
        # Handle the case where multiple products have the same slug
        # For example, you could select the first product:
        product = Product.objects.filter(slug=slug).first()


    delivery_date = None  # Default value for delivery date

    if request.method == 'POST':
        pincode_form = PincodeForm(request.POST)
        if pincode_form.is_valid():
            pincode = pincode_form.cleaned_data['pincode']
            delivery_date = calculate_delivery_date(pincode) 

    similar_products = Product.objects.filter(Sub_category=product.Sub_category).exclude(id=product.id)
    comments = Comment.objects.filter(product=product)
    avg_rating = comments.aggregate(avg_rating=models.Avg('numeric_rating'))['avg_rating']
    user_rating = None  # You can implement this based on user authentication

    variants = Variants.objects.filter(product=product)
    variant_details = {}
    variant_images = []
    unique_colors = []
    unique_sizes = []

    if variants.exists():
        variant = variants.first()
        variant_details = {
            'id': variant.id,
            'title': variant.title,
            'color': variant.color.name if variant.color else '',
            'size': variant.size.name if variant.size else '',
            'price': variant.price,
            'image_url': variant.image_id if variant.image_id else '',
        }
        unique_colors = variants.values_list('color__name', flat=True).distinct()
        unique_sizes = variants.values_list('size__name', flat=True).distinct()
        variant_images = Variant_image.objects.filter(variant=variant.id)

    comments_list = list(comments.values())
    product_images = product.product_image_set.all()
    cart_products, cart_products_ids_list, cart_count = cart_function(request)

    context = {
        'product_images': product_images,
        'product': product,
        'comments': comments_list,
        'avg_rating': avg_rating,
        'user_rating': user_rating,
        'product_variant': variant_details,
        'variant_images': variant_images,
        'cart_products': cart_products,
        'cart_count': cart_count,
        'similar_products': similar_products,
        'cart_products_ids_list': cart_products_ids_list,
        'unique_colors': unique_colors,
        'unique_sizes': unique_sizes,
        'color_radio': color,
        'size_radio': size,
        "main_category": categories_function(request)[0],
        "category": categories_function(request)[1],
        "Sub_category": categories_function(request)[2],
        'delivery_date': delivery_date,
    }

    # Update recently viewed products
    viewed_products_ids = request.session.get('viewed_products', [])
    if product.id not in viewed_products_ids:
        viewed_products_ids.append(product.id)
        request.session['viewed_products'] = viewed_products_ids

    # Fetch viewed products
    viewed_products = Product.objects.filter(id__in=viewed_products_ids)[::6]
    context['viewed_products'] = viewed_products

    # Update scroll position
    scroll_position = request.GET.get('scroll_position', 0)
    context['scroll_position'] = scroll_position

    return render(request, 'Main/product_detail.html', context=context)








# def prod_detail(request, slug,product_id=None, variant_id=None, color=None, size=None):
#     product = get_object_or_404(Product, slug=slug, id=product_id)
#     variants = Variants.objects.filter(product=product)
#     variant = variants.first()
#     variant_details = [
#         {
#             'id': variant.id,
#             'title': variant.title,
#             'color_name': variant.color.name if variant.color else '',
#             'size': variant.size.name if variant.size else '',
#             'price': variant.price,
#             'image_url': variant.image_id.url if variant and variant.image_id else '',
#         }
#     ]
#     product_variant = variant_details[0]
#     variant_images = Variant_image.objects.filter(variant=product_variant['id'])
#     cart_products,cart_products_ids_list,cart_count = cart_function(request)
#     product_dict = {
#         'id': product.id,
#         'slug':product.slug,
#         'name': product.name,
#         'total_quantity':product.total_quantity,
#         'Availability':product.Availability,
#         'price':product.price,
#         'Product_info':product.Product_info,
#         'Description':product.Description,
#     }
#     unique_colors = variants.values_list('color__name', flat=True).distinct()
#     unique_sizes = variants.values_list('size__name', flat=True).distinct()
#     color_radio = variant.color.name
#     size_radio = variant.size.name
#     default_color = unique_colors[0] if unique_colors else ''
#     default_size = unique_sizes[0] if unique_sizes else ''
#     context = {
#         'product':product,
#         'product_variant': product_variant,
#         'variant_images': variant_images,
#         'cart_products_ids_list':cart_products_ids_list,
#         'unique_colors': unique_colors,
#         'unique_sizes': unique_sizes,
#         "color_radio":color_radio,
#         "size_radio":size_radio,
#         'color_radio': default_color,  # Set default color value
#         'size_radio': default_size,
#         }

#     print("----------------------",request.method)
#     if request.method == 'POST':
#         product = get_object_or_404(Product, id=product_id)
#         # data = json.loads(request.body.decode('utf-8'))
#         # v_size = data.get('size')
#         # v_color = data.get('color')
#         v_size = request.POST.get('size')
#         v_color = request.POST.get('color')
#         variants = Variants.objects.filter(product=product)

#         if v_color and v_size:
#             content = {}
#             selected_variants = variants.filter(color__name=v_color, size__name=v_size)

#             if selected_variants.exists():
#                 selected_variant = selected_variants.first()
#             else:
#                 selected_variant = None

#             variant_details = {
#                 'id': selected_variant.id if selected_variant else None,
#                 'title': selected_variant.title if selected_variant else '',
#                 'color': selected_variant.color.name if selected_variant and selected_variant.color else '',
#                 'size': selected_variant.size.name if selected_variant and selected_variant.size else '',
#                 'price': selected_variant.price if selected_variant else 0,
#                 'image_url': selected_variant.image_id.url if selected_variant and selected_variant.image_id else '',
#             }

#             variant_images = Variant_image.objects.filter(variant=variant_details['id']) if selected_variant else []



#             main_category, category, Sub_category = categories_function(request)
#             content.update({
#                 "main_category": main_category,
#                 "category": category,
#                 "Sub_category": Sub_category
#             })

#             scroll_position = request.GET.get('scroll_position', 0)
#             content['scroll_position'] = scroll_position

#             response_data = {
#                 'message': 'Data processed successfully',
#                 'content': {
#                     'product_variant': variant_details,
#                     'variant_images': variant_images,
#                 },  # Include the context in the response for debugging
#             }

#             print("----------------------",response_data)

#             return JsonResponse(response_data)

#     # Include other data in the context (assuming these functions are defined elsewhere)
#     main_category, category, Sub_category = categories_function(request)
#     context.update({
#         "main_category": main_category,
#         "category": category,
#         "Sub_category": Sub_category
#     })

#     scroll_position = request.GET.get('scroll_position', 0)
#     context['scroll_position'] = scroll_position

#     # print(context,"----------")

#     return render(request, 'Main/product_detail.html', context=context)

# The view for handling the form submission asynchronously
def update_variants(request, slug, product_id=None):
    product = get_object_or_404(Product, slug=slug, id=product_id)
    variants = Variants.objects.filter(product=product)

    selected_color = request.GET.get('color')
    selected_size = request.GET.get('size')

    if selected_color:
        variants = variants.filter(color__name=selected_color)
    if selected_size:
        variants = variants.filter(size__name=selected_size)

    variant_details = [
        {
            'id': variant.id,
            'title': variant.title,
            'color_name': variant.color.name if variant.color else '',
            'size': variant.size.name if variant.size else '',
            'price': variant.price,
            'image_url': variant.image_id.url if variant and variant.image_id else '',
        }
        for variant in variants
    ]

    data = {
        'variants': variant_details,
    }

    return JsonResponse(data)



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


# def get_variant_details(request):
#     if request.method == 'GET':
#         variant_id = request.GET.get('variant_id')
#         try:
#             variant = Variants.objects.get(id=variant_id)
#             data = {
#                 'price': variant.price,
#                 'image_url': variant.image().url if variant.image() else '',
#             }
#             return JsonResponse(data)
#         except Variants.DoesNotExist:
#             return JsonResponse({'error': 'Variant not found'}, status=404)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=400)

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

        cart_products, cart_products_ids_list, cart_count = cart_function(request)

        packing_cost = 0
        tax = 0

        for item in cart_products:
            if 'packing_cost' in item and item['packing_cost'] is not None:
                packing_cost += item['packing_cost']

            if 'variant_price' in item and 'tax' in item and item['variant_price'] is not None and item['tax'] is not None:
                tax += (item['variant_price'] * item['tax']) / 100

        coupon = None
        valid_coupon = None
        invalid_coupon = None

        if request.method == 'GET':
            coupon_code = request.GET.get('c')

            if coupon_code:
                try:
                    coupon = Coupon.objects.get(code=coupon_code)
                    valid_coupon = "Is a valid coupon code"
                except Coupon.DoesNotExist:
                    invalid_coupon = "Invalid coupon code"
        subtotals = 0
        for value in cart_products:
            variant_total = calculate_variant_total(value['id'])  # Assuming you have a function to calculate variant total
            subtotals += value['quantity'] * variant_total

        total_amount = subtotals + tax + packing_cost + 70

        if valid_coupon:
            coupon_discount = (subtotals * coupon.discount) / 100
            total_amount -= coupon_discount
        main_category, category, sub_category = categories_function(request)

        params = {
            'packing_cost': packing_cost,
            'tax': tax,
            'coupon': coupon,
            'valid_coupon': valid_coupon,
            'invalid_coupon': invalid_coupon,
            'order_id': order_id,
            'payment': payment,
            # 'user':user,
            'subtotals': subtotals,
            'cart_products': cart_products,
            'total_amount':total_amount,
            'main_category': main_category,
        'category': category,
        'sub_category': sub_category,
        }
        return render(request, 'Main/checkout.html', params)




def clear_cart(request):
    # Implement your logic to clear the cart here
    # You can use the existing clear_cart function or modify it as needed
    user = request.user
    cart = User_cart.objects.get(user=user)
    cart.cart_items.all().delete()






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
        # amount=request.POST.get('amount')
        # amount = request.POST.get('total_amount')
        amount = 10
        order_id = request.POST.get('order_id')
        payment=request.POST.get('payment')
        # prnt(firstname,lastname,email,city,zip_code,additional_info,address,phone,amount,order_id,payment)
        print("Amount:", amount)
        print("Order ID:", order_id)
        print("Payment:", payment)
   
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
          
        )
        order.save()
        # Assuming you have the total amount in the form data

        params = {
            'user':user,
            'amount':amount,
            'order_id':order_id,
           
            }
        return render(request, 'Main/place_order.html',context=params)


def payment_success_view(request):
    total_amount = request.POST.get('total_amount')
    order_id = request.POST.get('order_id')
    payment_id = request.POST.get('razorpay_payment_id')
    signature = request.POST.get('razorpay_signature')
    params_dict = {
        'razorpay_order_id': order_id,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
    }
    try:
        client.utility.verify_payment_signature(params_dict)
        # Payment signature verification successful
        # Perform any required actions (e.g., update the order status)
        clear_cart(request)
        return redirect('/')
    except razorpay.errors.SignatureVerificationError as e:
        # Payment signature verification failed
        # Handle the error accordingly
        return redirect('/')















def My_Account(request):
    # return render(request,'../templates/Error_pages/404.html')
    main_category, category, sub_category = categories_function(request)
    cart_products,cart_products_ids_list,cart_count = cart_function(request)
    params ={
        'cart_products': cart_products,
        'cart_count':cart_count,
        'cart_products_ids_list':cart_products_ids_list,
        'main_category': main_category,
        'category': category,
        'sub_category': sub_category,
        }

    return render(request,'../templates/Main/profile.html',context=params)


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



def faq_view(request):
   return render(request,'../templates/faq.html')





def image_courtesy(request):
    return render(request,'../templates/Main/imagecourtesy.html')









from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from Ecommerceapp.models import Variants
from django.http import JsonResponse


def wishlist_view(request, product_variant_id):
    user = request.user
    variant = get_object_or_404(Variants, id=product_variant_id)

    # Check if the variant is already in the user's wishlist
    if Mylist.objects.filter(user=user, product_variant_id=product_variant_id).exists():
        return JsonResponse({'status': 'error', 'message': 'Product variant already in wishlist'})

    # Fetch the variant image
    variant_image = variant.image_id
    product_variant_name = variant.title  # Use the correct attribute name

    # Create a new wishlist item for the variant
    wishlist_item = Mylist.objects.create(
        user=user,
        product_variant_id=product_variant_id,
        product_variant_image=variant_image,
        product_variant_name=product_variant_name
    )

    # Return a success JSON response
    return JsonResponse({'status': 'success', 'message': 'Product variant added to wishlist'})


# def wishlist_delete(request, wishlist_item_id):
#     user = request.user

#     # Check if the wishlist item belongs to the user
#     wishlist_item = get_object_or_404(Mylist, id=wishlist_item_id, user=user)

#     # Delete the wishlist item
#     wishlist_item.delete()

#     # Return a success JSON response
#     return JsonResponse({'status': 'success', 'message': 'Wishlist item deleted'})



from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Mylist, Variants

def delete_from_wishlist(request, product_variant_id):
    user = request.user
    variant = get_object_or_404(Variants, id=product_variant_id)

    # Check if the variant is in the user's wishlist
    wishlist_item = Mylist.objects.filter(user=user, product_variant_id=product_variant_id).first()

    if not wishlist_item:
        return JsonResponse({'status': 'error', 'message': 'Product variant not found in wishlist'})

    # Delete the wishlist item
    wishlist_item.delete()

    # Return a success JSON response
    return JsonResponse({'status': 'success', 'message': 'Product variant removed from wishlist'})



def wishlist_page(request):
    user = request.user
    wishlist_items = Mylist.objects.filter(user=user)
    print(len(wishlist_items))  # Print the number of wishlist items
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


def payment_view(request):
    # Assuming you have logic to calculate the total amount dynamically
    total_amount = total_amount(request)  # Function to calculate total amount
    order_id = initiate_payment(total_amount)
    context = {
        'order_id': order_id,
        'total_amount': total_amount
    }
    return render(request, 'place_order.html', context)

def initiate_payment(amount, currency='INR'):
   data = {
       'amount': amount * 100,  # Razorpay expects amount in paise (e.g., 100 INR = 10000 paise)
       'currency': currency,
       'payment_capture': '1'  # Auto capture the payment after successful authorization
   }
   response = client.order.create(data=data)
   return response['id']





def seller(request):
    return render(request,'../templates/Main/seller.html')


def startselling(request):
    return render(request,'../templates/Main/startselling.html')
def cancellation(request):
    return render(request, 'Main/cancellation.html')