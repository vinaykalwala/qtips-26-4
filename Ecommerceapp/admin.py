from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from .models import *
from django import forms
import admin_thumbnails
# from .forms import ProductAdminForm
from django.urls import reverse
from django.http import HttpResponseRedirect

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

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name','email','phone','address','gender']


class VariantImageInline(admin.TabularInline):
    list_display = ('variant.title',)
    search_fields = ['variant.title']
    model = Variant_image
    extra = 3
    show_change_link = True
class VariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('display_image',)

    extra = 1
    show_change_link = True
class ProductsAdmin(admin.ModelAdmin):
    # form = ProductAdminForm
    inlines = [ProductImageInline, VariantsInline, AdditionalInfoInline]
    list_display = ('name', 'display_image', 'price', 'Category', 'Sub_category', 'Section')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('display_image',)
    list_per_page = 50
    search_fields = ['name', 'Category__name', 'Sub_category__name', 'Section__name']

    def display_image(self, obj):
        if obj.image and obj.image.url:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        else:
            return "No Image"

    display_image.short_description = 'Image'
    actions = ['duplicate_selected']

    def duplicate_selected(self, request, queryset):
        for original_product in queryset:
            # Duplicate the product
            new_product = Product.objects.create(
                name=original_product.name,
                price=original_product.price,
                Category=original_product.Category,
                Sub_category=original_product.Sub_category,
                Section=original_product.Section,
                image = original_product.image,
                brand = original_product.brand,
                Availability = original_product.Availability,
                Discount = original_product.Discount,
                tax = original_product.tax,
                packing_cost = original_product.packing_cost,
                Product_info = original_product.Product_info,
                model_name = original_product.model_name,
                Tags = original_product.Tags,
                Description = original_product.Description,
                total_quantity = original_product.total_quantity,
                # Duplicate other fields as needed
            )

            # Duplicate the variants associated with the original product
            for original_variant in original_product.variants_set.all():
                Variants.objects.create(
                    product=new_product,
                    title=original_variant.title,
                    color=original_variant.color,
                    size=original_variant.size,
                    price=original_variant.price,
                    quantity=original_variant.quantity,
                    image_id = original_variant.image_id,
                    # Duplicate other fields as needed
                )

    duplicate_selected.short_description = "Duplicate selected products"

    def save_model(self, request, obj, form, change):
        # Check if the user wants to duplicate the product
        if '_duplicate' in request.POST:
            # Manually duplicate variants when saving a single product
            obj.pk = None
            obj.save()

            for original_variant in obj.variants_set.all():
                Variants.objects.create(
                    product=obj,
                    title=original_variant.title,
                    color=original_variant.color,
                    size=original_variant.size,
                    price=original_variant.price,
                    quantity=original_variant.quantity,
                    # Duplicate other fields as needed
                )

            return

        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        # Duplicate variants when saving multiple products
        if '_duplicate' in request.POST:
            for formset in formsets:
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.pk = None
                    instance.product = obj  # Change form.instance to obj
                    instance.save()

        super().save_related(request, form, formsets, change)




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
    inlines = [VariantImageInline]
    list_filter = ['product']
    # list_display = ['title', 'product', 'color_name', 'size', 'price', 'quantity','display_image']
    search_fields = ['title','product__name', 'color__name', 'size__name']
    list_display = ['title', 'product', 'color_name', 'size', 'price', 'quantity', 'display_image']

    def display_image(self, obj):
        return obj.display_image()

    display_image.short_description = 'Image'
# Partners
class VariantImageInlineFormSet(forms.models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = Variant_image.objects.none()

class DealOfDayAdminForm(forms.ModelForm):
    class Meta:
        model = Deal_of_the_day
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DealOfDayAdminForm, self).__init__(*args, **kwargs)
        # Customize the product field to display product IDs
        self.fields['product'].label_from_instance = lambda obj: f"{obj.id} - {obj.name}" if obj.name else str(obj.id)

class DealOfTheDayAdmin(admin.ModelAdmin):
    model = Deal_of_the_day
    fields = ['product', 'discount', 'deal_datetime','deal_end_time']

admin.site.register(Deal_of_the_day, DealOfTheDayAdmin)
admin.site.register(Partners)
admin.site.register(Top_Featured)
admin.site.register(Moving_text)

# Register your models here.
admin.site.register(Contact)
# admin.site.register(OrderUpdate)
admin.site.register(Discount_deal)
admin.site.register(Order, OrderAdmin)
admin.site.register(Tag)
# admin.site.register(Order_item)
admin.site.register(Brands)
admin.site.register(Sliders)
admin.site.register(Header_Icons)

admin.site.register(Variant_image)
admin.site.register(Banners)

# CATEGORIES
admin.site.register(Main_categorie)
admin.site.register(Categorie)
admin.site.register(Sub_categorie)

# PRODUCTS & VIEWS
admin.site.register(Product, ProductsAdmin)
admin.site.register(Comment)
# admin.site.register(Rating)
admin.site.register(Product_image,ImageAdmin)
admin.site.register(Additional_info)
admin.site.register(Section)
admin.site.register(Size, SizeAdmin)
admin.site.register(Variants, VariantsAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Coupon)
admin.site.register(Profile, ProfileAdmin)

# CART
