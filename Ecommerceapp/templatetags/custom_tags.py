# custom_tags.py
from django import template
import os

register = template.Library()

@register.simple_tag
def get_category_image_url(category):
    if category.image:
        # Check if the local image file exists
        local_path = os.path.join('media', str(category.image))
        if os.path.exists(local_path):
            return category.image
        else:
            # Use the AWS S3 URL if the local file doesn't exist
            return category.image.url
    else:
        # No image associated, return an empty string or a placeholder URL
        return ''

@register.simple_tag
def get_product_image_url(product):
    if product.image:
        local_path = os.path.join('media', str(product.image))
        if os.path.exists(local_path):
            return product.image
        else:
            return product.image.url  # Replace this with the actual AWS S3 URL retrieval logic
    else:
        return ''

@register.simple_tag
def get_product_image(product):
    if hasattr(product, 'image') and product.image:
        local_path = os.path.join('media', str(product.image))
        if os.path.isfile(local_path):
            return f'/media/{product.image}'  # Local media file
        else:
            # Replace this with the actual AWS S3 URL retrieval logic
            return f'https://qtipstorebucket.s3.amazonaws.com/{product.image.url}'
    else:
        return ''  # Handle the case where there is no image


@register.simple_tag
def get_product_variant_image_url(product_variant):
    if product_variant['image_url']:
        local_path = os.path.join('media', str(product_variant['image_url']))
        real_path = os.path.abspath(local_path)

        print(f"Constructed Path: {local_path}")
        print(f"Real Path: {real_path}")

        if os.path.exists(real_path):
            print("Local file exists!")
            return f"/{local_path}"
        else:
            print("Local file does not exist.")
            return product_variant['image_url'].url

    else:
    #     # No image associated, return an empty string or a placeholder URL
        return ''
@register.simple_tag
def get_variant_image_url(variant_image):
    if hasattr(variant_image, 'image') and variant_image.image:
        # Check if 'image' is a file path or a field/property
        if isinstance(variant_image.image, str):
            # If 'image' is a string, it's a file path
            image_filename = os.path.basename(variant_image.image.replace(' ', '_'))
            local_path = os.path.abspath(os.path.join('media', image_filename))

            if os.path.isfile(local_path):
                return f'/media/{image_filename}'  # Local media file
            else:
                # Replace this with the actual AWS S3 URL retrieval logic
                return get_aws_s3_url(image_filename)
        else:
            # If 'image' is not a string, it's assumed to be a field/property
            # Replace this with the actual logic to retrieve the URL from the field/property
            if hasattr(variant_image.image, 'url'):
                return variant_image.image.url
            else:
                return ''  # Handle the case where there is no image
    else:
        return ''  # Handle the case where there is no image

def get_aws_s3_url(image_filename):
    # Replace this with the actual AWS S3 URL retrieval logic
    return f'https://qtipstorebucket.s3.amazonaws.com/{image_filename}'
