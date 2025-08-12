from django.db import models
from django.utils.text import slugify
import random 
import os
import string


def product_image_path(instance,filename):
    ext = os.path.splitext(filename)[1]
    random_string = ''.join(random.choice(string.ascii_letters,k=10))
    return f"products/image-{random_string}{ext}"

class Product(models.Model):
    title =models.CharField(max_length=200)

    descriptions = models.CharField(max_length=200)

    image = models.ImageField(upload_to=product_image_path)
    
    slug  = models.SlugField(unique=True,blank=True)


