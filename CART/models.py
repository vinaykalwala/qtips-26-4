from django.db import models
from Ecommerceapp.models import *

# Create your models here.
class User_Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('CartItem', related_name='cart_items')

    def __str__(self):
        return self.user.email

class CartItem(models.Model):
    cart = models.ForeignKey(User_Cart, on_delete=models.CASCADE, related_name='cart_items')
    variant = models.ForeignKey('Ecommerceapp.Variants', on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=1)

    # Additional fields from Variant model
    variant_title = models.CharField(max_length=100,blank=True)
    variant_price = models.FloatField(null=True)
    variant_image = models.ImageField(null=True, upload_to='Cart_images',blank=True)
    variant_size = models.CharField(max_length=50,blank=True)
    variant_color = models.CharField(max_length=50,blank=True)

    # Additional fields from Product model
    price = models.FloatField(null=True,blank=True)
    product_id = models.IntegerField(default=0)
    packing_cost = models.FloatField(default=1)
    tax = models.FloatField(default=1,null=True)
    model_name = models.CharField(max_length=120,blank=True,null=True)
    brand_name = models.CharField(max_length=50, null=True,blank=True)
    tag_name = models.CharField(max_length=50,blank=True,null=True)

    def save(self, *args, **kwargs):
       if self.variant:
        print(f"Variant: {self.variant}")
        # Populate fields from Variant
        self.variant_title = self.variant.title
        self.variant_price = self.variant.price
        self.variant_image = self.variant.image_id
        self.variant_size = self.variant.size.name
        self.variant_color = self.variant.color_name

        # Populate fields from Product
        if self.variant.product:
            self.product_id = self.variant.product.id
            self.packing_cost = self.variant.product.packing_cost
            self.tax = self.variant.product.tax
            self.model_name = self.variant.product.model_name
            self.brand_name = self.variant.product.brand.Brand_name if self.variant.product.brand else ''
            self.tag_name = self.variant.product.Tags.name if self.variant.product.Tags else ''

            super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.cart.user.email} -> {self.variant.product.name} - {self.variant.size} - {self.variant.color}"
