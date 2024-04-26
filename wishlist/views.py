# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404
# from django.shortcuts import render
# from .models import Mywishlist

# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404
# from django.shortcuts import render
# from django.conf import settings  # Import Django settings

# def wishlist_view(request, product_variant_id):
#     if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#         # Retrieve the product variant instance
#         product_variant_instance = get_object_or_404(Mywishlist, product_variant_id=product_variant_id)

#         # Logic to add the product variant to the wishlist
#         # This can vary based on your application's requirements

#         return JsonResponse({'message': 'Product variant added to wishlist successfully'}, status=200)
#     else:
#         return JsonResponse({'error': 'Invalid request'}, status=400)

# def wishlist_page(request):
#     # Add your logic to retrieve wishlist items
#     wishlist_items = Mywishlist.objects.all()  # Retrieve all wishlist items

#     return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


