# from django.db import models
# from django.contrib.auth.models import User


# class Mywishlist(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product_variant_id = models.CharField(max_length=100)
#     product_variant_image = models.ImageField(upload_to='wishlist_variant_images', null=True, blank=True)

#     def __str__(self):
#         return f"Wishlist Item for {self.user.username}: {self.product_variant_id}"