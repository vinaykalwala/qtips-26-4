from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save
import uuid
import hashlib
from django.utils.crypto import get_random_string
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from autoslug import AutoSlugField

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager


class Main_categorie(models.Model):
    name = models.CharField(null=True,max_length=200)
    image = models.ImageField(upload_to='Main_category_images',null=True,blank=True)
    slug = models.SlugField(max_length=255,null=True, unique=True,blank=True)


    def __str__(self):
        return self.name

class Categorie(models.Model):
    main_category = models.ForeignKey(Main_categorie,on_delete=models.CASCADE)
    name = models.CharField(null=True,max_length=200)
    image = models.ImageField(upload_to='Subcategory_images',null=True,blank=True)
    slug = models.SlugField(max_length=255, unique=True,null=True,blank=True)
    popular=models.BooleanField(default=False)


    def __str__(self):
        return self.name + " -> " + self.main_category.name

class Sub_categorie(models.Model):
    category = models.ForeignKey(Categorie,on_delete=models.CASCADE)
    name = models.CharField(null=True,max_length=200)
    slug = models.SlugField(max_length=255, unique=True,null=True,blank=True)


    def __str__(self):
        return self.name +"->"+self.category.name+"->"+ self.category.main_category.name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    
    def _str_(self):
        return self.full_name

class Coupon(models.Model):
    code = models.CharField(null=True,max_length=200)
    discount = models.IntegerField(null=True,)

    def __str__(self):
        return self.code

class Tag(models.Model):
    name = models.CharField(null=True,max_length=200)

    def __str__(self):
        return self.name




class Color(models.Model):
    code = models.CharField(null=True,max_length=100)
    name = models.CharField(max_length=200)


    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color: {}">Color </p>'.format(self.code))
        else:
            return ""

    def __str__(self):
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




class Discount_deal(models.Model):
    name = models.CharField(null=True,max_length=200)
    Discount = models.FloatField(default=0)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.id} {self.name}"

class Sliders(models.Model):


    image = models.ImageField(null=True,upload_to='slider_imgs')
    Discount_deal = models.ForeignKey(Discount_deal,on_delete=models.CASCADE)
    Sale = models.IntegerField(null=True,)
    Discount = models.IntegerField(null=True)
    Description_1 = models.CharField(null=True,max_length=100)
    Description_2 = models.CharField(null=True,max_length=200)
    Link = models.CharField(null=True,max_length=2000)

    def __str__(self):
        return self.Description_1

class Header_Icons(models.Model):
    Category = models.ForeignKey(Categorie,on_delete=models.CASCADE,null=True)
    # name = models.CharField(max_length=200,null=True)
    Icon = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.Category.name


class Section(models.Model):
    name = models.CharField(null=True,max_length=150)
    contains_products = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Moving_text(models.Model):
    text = models.CharField(null=True,max_length=300)
    section = models.ForeignKey(Section,on_delete=models.CASCADE,null=True,blank=True)
    date=models.DateTimeField(null=True,default=timezone.now)

    def __str__(self):
        return self.text

class Banners(models.Model):


    image = models.ImageField(null=True,upload_to='sm_banners')
    Key_point_2 = models.CharField(null=True,max_length=100)
    Discount_deal = models.ForeignKey(Discount_deal, on_delete=models.CASCADE,null=True,)
    Key_point_1 = models.CharField(null=True,max_length=200)
    Discount = models.IntegerField(null=True,blank=True)
    Link = models.CharField(max_length=2000,null=True,blank=True)
    section = models.ForeignKey(Section,null=True,on_delete=models.CASCADE)
    # category = models.ForeignKey(Categorie,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.Key_point_2




class Product(models.Model):
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    name = models.CharField(null=True, max_length=500)
    # image = models.ImageField(null=True, upload_to='Product_images')
    def get_upload_path(instance, filename):
        # Generate a folder name based on the product name
        folder_name = slugify(instance.name)[:30]

        # Define the upload path using the folder_name
        upload_path = f"Product_images/{folder_name}"

        # Return the final upload path
        return f"{upload_path}/{filename}"
    image = models.ImageField(blank=True,null=True,upload_to=get_upload_path)
    total_quantity = models.IntegerField(null=True,blank=True)
    Availability = models.IntegerField(null=True,blank=True)
    price = models.FloatField(null=True,blank=True)
    Discount = models.IntegerField(null=True,blank=True)
    tax = models.FloatField(null=True, blank=True)
    packing_cost = models.FloatField(null=True, blank=True)
    Product_info = RichTextField(null=True,blank=True)
    model_name = models.CharField(null=True, max_length=120,blank=True)
    Category = models.ForeignKey('Categorie', null=True, on_delete=models.CASCADE,blank=True)
    Deals = models.ForeignKey('Discount_deal', null=True, on_delete=models.CASCADE,blank=True)
    Sub_category = models.ForeignKey('Sub_categorie', on_delete=models.CASCADE, null=True, blank=True)
    Tags = models.ForeignKey('Tag', null=True, blank=True, on_delete=models.CASCADE)
    Description = RichTextField(null=True,blank=True)
    Section = models.ForeignKey('Section', null=True, on_delete=models.DO_NOTHING,blank=True)
    brand = models.ForeignKey('Brands', on_delete=models.CASCADE, null=True, blank=True)
    original_price = models.FloatField(null=True, blank=True)
    cod = models.BooleanField(default=False,null=True)
    seller = models.CharField(max_length=255)
    seller_description = models.CharField(max_length=255, null=True, blank=True)
    seller_since = models.DateField(null=True, blank=True)

    rating = models.FloatField(default=0.0,null=True,blank=True)
    color=models.BooleanField(default=False,null=True)
    size=models.BooleanField(default=False,null=True)

    def update_average_rating(self):
        # Calculate and update the average rating for the product using Comment model
        ratings = Comment.objects.filter(product=self)
        if ratings.exists():
            average_rating = ratings.aggregate(models.Avg('numeric_rating'))['numeric_rating__avg']
            self.rating = round(average_rating, 1)  # Round to one decimal place
        else:
            self.rating = 0.0

        self.save()

    def variants(self):
        # Return the variants related to this product
        return Variants.objects.filter(product=self)

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url) if self.image else '')

    image_tag.short_description = 'Image'


    def quantity_sold(self):
        return self.total_quantity - self.Availability

    def __str__(self):
        return f"{self.id} {self.name}"


    def save(self, *args, **kwargs):
        # Your existing save logic
        if not self.slug:
            self.slug = self.generate_custom_id()
        super().save(*args, **kwargs)

    def generate_custom_id(self):
        from django.utils.crypto import get_random_string
        current_time = timezone.now()
        timestamp_milliseconds = int(current_time.timestamp() * 1000)

        # Modify this part according to your needs
        sliced_name = self.name.split()[0]
        return f"qtip{slugify(sliced_name)}pd{timestamp_milliseconds}_{get_random_string(5)}"
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={'slug': self.slug})

    def custom_id(self):
        return f"Custom ID: {self.slug}"

    def get_average_rating(self):
        # Calculate the average rating for the product using Comment model
        ratings = Comment.objects.filter(product=self)
        if ratings.exists():
            average_rating = ratings.aggregate(models.Avg('numeric_rating'))['numeric_rating__avg']
            return round(average_rating, 1)  # Round to one decimal place
        return 0.0

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_custom_id()

        super().save(*args, **kwargs)  # Save the Product instance

        # Save associated Product_image instances
        if self.image:
            Product_image.objects.create(product=self, image=self.image)

    # ... other methods ...

    class Meta:
        db_table = "app_Product"


from django.db import models
from .models import Product  # Assuming Product model is imported

class Deal_of_the_day(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount = models.FloatField(default=0)
    deal_datetime = models.DateTimeField(null=True, blank=True)
    deal_end_time = models.DateTimeField(null=True, blank=True)  # New field

    def __str__(self):
        return self.product.name







    def save(self, *args, **kwargs):
        # Apply discount to the associated product's price
        self.product.original_price = self.product.price
        discounted_price = self.product.price - (self.product.price * (self.discount / 100))
        self.product.price = discounted_price
        self.product.save()

        super().save(*args, **kwargs)

class Top_Featured(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    def __str__(self):
        return self.product.name

# class WishList(models.Model):



class Product_image(models.Model):
    product = models.ForeignKey(Product,null=True,on_delete=models.CASCADE,blank=True)
    image = models.ImageField(null=True, upload_to='Product_images',blank=True)

    def __str__(self):
        return f"{self.product.name} - Image {self.id}"

# VARIANTS

def get_variant_image_upload_path(instance, filename):
    # Generate a folder structure based on the product name, color, and size
    product_name_folder = slugify(instance.variant.product.name)[:30]  # Limit to 50 characters
    variant_folder = f"{slugify(instance.variant.size)} - {slugify(instance.variant.color_name)}"

    # Define the upload path using the folder structure
    upload_path = f"Product_images/{product_name_folder}/{variant_folder}/Variant_images"

    # Use a hash-based filename to ensure uniqueness and manage length
    file_hash = hashlib.md5(filename.encode()).hexdigest()[:3]  # Limit to 8 characters
    short_filename = f"{file_hash}.jpg"  # Adjust the file extension as needed

    # Return the final upload path
    return f"{upload_path}/{short_filename}"

class Variant_image(models.Model):
    variant = models.ForeignKey('Variants', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, editable=False, blank=True, null=True)
    def get_upload_path(instance, filename):
        # Generate a folder structure based on the product name, color, and size
        product_name_folder = slugify(instance.variant.product.name)[:30]
        variant_folder = f"{instance.variant.size} - {instance.variant.color_name}"

        # Define the upload path using the folder structure
        upload_path = f"Product_images/{product_name_folder}/{variant_folder}/Variant_imgs"
        file_hash = hashlib.md5(filename.encode()).hexdigest()[:5]  # Limit to 8 characters
        short_filename = f"{file_hash}.jpg"

        # Return the final upload path with a separate folder for each variant
        return f"{upload_path}/{filename}"
    image = models.ImageField(null=True, upload_to=get_upload_path,blank=True)

    def __str__(self):
        return f"{self.variant.title} - Image {self.id}"

    def save(self, *args, **kwargs):
        self.product = self.variant.product
        super().save(*args, **kwargs)


class Variants(models.Model):
    slug = AutoSlugField(populate_from='title', unique=True, null=True, blank=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    color = models.ForeignKey('Color', on_delete=models.SET_NULL, blank=True, null=True)
    size = models.ForeignKey('Size', on_delete=models.SET_NULL, blank=True, null=True)
    def get_upload_path(instance, filename):
        # Generate a folder structure based on the product name, color, and size
        product_name_folder = slugify(instance.product.name)[:30]
        variant_folder = f"{instance.size} - {instance.color_name}"

        # Define the upload path using the folder structure
        upload_path = f"Product_images/{product_name_folder}/{variant_folder}"

        # Return the final upload path with a separate folder for each variant
        return f"{upload_path}/{filename}"

    image_id = models.ImageField(
        null=True,
        blank=True,
        upload_to=get_upload_path,  # Use a function for dynamic upload path
    )
    quantity = models.IntegerField(default=1)
    price = models.FloatField(default=0)
    # variant_images = models.ManyToManyField(Variant_image)

    def __str__(self):
        return self.title

    def display_image(self):
        if self.image_id and self.image_id.url:
            return format_html('<img src="{}" width="50" height="50" />', self.image_id.url)
        else:
            return "No Image"
    display_image.short_description = 'Image'

    @property
    def color_name(self):
        return self.color.name if self.color else ''

    @classmethod
    def create_variant(cls, product, title, color, size, image_id, quantity, price):
        new_variant = cls.objects.create(
            title=title,
            product=product,
            color=color,
            size=size,
            image_id=image_id,
            quantity=quantity,
            price=price
        )
        new_variant.slug = new_variant.generate_custom_id()
        new_variant.save()
        return new_variant
    id = models.CharField(max_length=50, primary_key=True, editable=False)

    def save(self, *args, **kwargs):
        # Generate custom ID if it doesn't exist
        if not self.id:
            timestamp_milliseconds = int(timezone.now().timestamp() * 1000)
            self.id = f"{timestamp_milliseconds}_{get_random_string(5)}"
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ['slug', 'product']

    def variants(self):
        return Variants.objects.filter(product=self)

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={'slug': self.slug})

    def related_variant_images(self):
        return Variant_image.objects.filter(variant=self)


@receiver(post_save, sender=Variant_image)
def update_variant_images(sender, instance, **kwargs):
    if instance.variant.color:
        # Find other variants of the same product and color
        other_variants = Variants.objects.filter(product=instance.variant.product, color=instance.variant.color).exclude(id=instance.variant.id)

        # Link the variant to the color's images
        for variant in other_variants:
            # Create variant images if they don't exist
            Variant_image.objects.get_or_create(variant=variant, image=instance.image)


class Additional_info(models.Model):
    product = models.ForeignKey(Product,null=True,on_delete=models.CASCADE)
    specification = models.CharField(null=True,max_length=120)
    detail = models.CharField(null=True,max_length=100)

    def __str__(self):
        return self.product.name



class Comment(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    numeric_rating = models.IntegerField(default=0, choices=[(i, i) for i in range(1, 6)])
    image = models.ImageField(upload_to='comment_images', null=True, blank=True)



    

from django.db import models

class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    email = models.EmailField(null=True)
    name = models.CharField(null=True, max_length=200)
    subject = models.CharField(null=True, max_length=500)
    message = models.TextField(null=True, max_length=1000)

    def __str__(self):
        return self.email if self.email else f"Contact {self.contact_id}"




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







from django.db import models
from django.contrib.auth.models import User


class Mylist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_variant_id = models.CharField(max_length=100)
    product_variant_image = models.ImageField(upload_to='wishlist_variant_images', null=True, blank=True)
    product_variant_name = models.CharField(max_length=255)  # New field for variant name

    def __str__(self):
        return f"Wishlist Item for {self.user.username}: {self.product_variant_id}"