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

    creat_at = models.DateTimeField(auto_now_add=True)
    
    slug  = models.SlugField(unique=True,blank=True,allow_unicode=True)
    
    categories = models.ManyToManyField("Category",related_name='products')

    warranties = models.ManyToManyField("Warranti",related_name='product',blank=True)


    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title,allow_unicode=True)
        return super().save(*args,**kwargs)



class Warranti(models.Model):
    name = models.CharField(max_length=300,unique=True)
    warranti_time = models.PositiveIntegerField()



class Review(models.Model):
    product = models.ForeignKey(Product ,on_delete=models.CASCADE ,related_name='reviews')

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    comment = models.TextField(blank=True)

    creat_at = models.DateTimeField(auto_now_add=True)

    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.title}"
    


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True ,blank=True, allow_unicode=True)

    def __str__(self):
        return f'Category |{self.title}'

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title,allow_unicode=True)
        return super().save(*args,**kwargs)


class ProductPakage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='pakage')

    price = models.IntegerField()

    coler = models.CharField(max_length=30)

    final_price = models.IntegerField(default=0)

    discount = models.IntegerField(default=0)
    
    is_availbale = models.BooleanField(default=True)

    product_number = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product} | {self.coler}"

    def save(self,*args,**kwargs):
        self.final_price = int(self.price - (self.price * self.discount/100))
        return super().save(*args,**kwargs)

# this class is attribute product 

class AttrbiuteProduct(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)


# image galery 

class ProductImage(models.Model):
    image = models.ImageField(upload_to=product_image_path)
    product =  models.ForeignKey(Product,on_delete=models.CASCADE, related_name="images")
