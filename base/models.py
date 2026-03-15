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

class Order(models.Model):
    order_id = models.CharField(max_length = 100)
    date = models.DateTimeField(auto_now_add = True)
    total = models.FloatField()
    name = models.CharField(max_length = 100)
    address = models.CharField(max_length = 255)
    city = models.CharField(max_length = 50)
    state = models.CharField(max_length = 20)
    email = models.EmailField()
    phone_number = models.CharField(max_length = 20)
    receipt = models.TextField()

    def __str__(self):
        return f"{self.order_id} for {self.name}"

class OrderItem(models.Model):
    product_name = models.CharField(max_length = 25)
    quantity = models.IntegerField()
    unit_price = models.CharField()
    order = models.ForeignKey(Order, related_name = "order_item", on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.product_name} in order {self.order.order_id}"
    

class Message(models.Model):
    message_sender = models.CharField(max_length = 255)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"Message from {self.message_sender}"
