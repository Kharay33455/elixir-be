from rest_framework.serializers import ModelSerializer, CharField
from .models import *


class ProductImageSerializer(ModelSerializer):

    class Meta:
        model = ProductImage
        exclude = ['id', 'product']
    
class ProductSerializer(ModelSerializer):
    product_img = ProductImageSerializer(many = True, read_only = True)

    class Meta:
        model = Product
        exclude = ['id']

class CartItemSerializer(ModelSerializer):
    product = CharField(source = "product.name", read_only = True)
    class Meta:
        model = CartItem
        exclude = ['id']