from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length = 25, unique = True)
    price = models.CharField(max_length = 10)
    times_sold = models.IntegerField(default = 0)
    description = models.TextField()

    def __str__(self):
        return f'{self.name}'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name = "product_img", on_delete = models.CASCADE)
    image = models.ImageField(upload_to="media/products")

    def __str__(self):
        return f"{self.product.name} image."


class CartItem(models.Model):
    cart_id = models.CharField(max_length = 100)
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = "product")
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} {self.product.name}(s) for {self.cart_id}"