from Ecommerceapp import views
from django.urls import path
from CART.views import *

# from .views import RelatedDataAPI


urlpatterns = [
    #Home
    path('',views.index,name="index"),
      path("profile/", views.My_Account, name="profile"),


    #PRODUCTS
    path('products/<int:sub_category_>/', views.PRODUCTS, name='PRODUCTS'),
    path('cats/', views.CATS, name="cats"),
    path('sub_cats/', views.SUBCATS, name='SUBCATS'),
    # path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('shipping_policy/', views.shipping_policy, name='shipping_policy'),
    path('payment_policy/', views.payment_policy, name='payment_policy'),
    path('return_refund/', views.return_refund, name='return_refund'),
    path('product_detail/<slug:slug>&<int:product_id>', views.prod_detail, name='product_detail'),

    path('faq/', views.faq_view, name='faq'),

    path('get_variant_details/', views.get_variant_details, name='get_variant_details'),
    path('rate_product/<slug:slug>/', views.rate_product, name='rate_product'),
    path('add_comment/<slug:slug>/', views.add_comment, name='add_comment'),
    path('get_colors/', views.get_colors, name='get_colors'),
    path('product_deals/<slug:slug>&<int:deal_id>&<int:banner_id>',views.product_deals,name='product_deals'),

    #Contact
    path('contact/',views.contact,name="contact"),
    path('about/',views.ABOUT,name="about"),
#     path('products/filter-data/', views.filter_products, name='filter-data'),

    #CHECKOUT
    path('checkout/',views.checkout,name='checkout'),
    path('place_order/',views.Placeorder,name='Placeorder'),
    path('payment/success/', views.payment_success_view, name='payment_success'),
    path('404/',views.handle_404,name='404'),
   #search
    path('search/',views.Search,name='search'),
    # path('search/', Search, name='search'),
    path('error/<int:status_code>/', views.error_handler, name='error_handler'),
    path('image_courtesy',views.image_courtesy, name='image_courtesy'),
     path('wishlist/<str:product_variant_id>/', views.wishlist_view, name='wishlist_view'),
    path('wishlist/', views.wishlist_page, name='wishlist_page'),  # Add this line for the wishlist page
    # path('wishlist/<int:product_variant_id>/delete/', views.delete_wishlist_item, name='wishlist-delete'),

    # path('wishlist/delete/<int:wishlist_item_id>/',views.wishlist_delete, name='wishlist_delete'),
    path('wishlist/delete/<str:product_variant_id>/', views.delete_from_wishlist, name='delete_from_wishlist'),

    #CART
    path('cart/add/<slug:slug>/', views.cart_add, name='cart_add'),
    path('cart/add_home/<slug:slug>/', views.cart_add_home, name='cart_add_home'),
    path('cart/add_shop/<slug:slug>/', views.cart_add_shop, name='cart_add_shop'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    path('seller/', views.seller, name='seller'),
     path('startselling/', views.startselling, name='startselling'),
     path('cancellation/', views.cancellation, name='cancellation'),
    

]
