from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
import os

@api_view(['GET'])
def index(request):
    products = Product.objects.prefetch_related("product_img").all()
    products_serialized = ProductSerializer(products, many = True).data
    context = {"products": products_serialized, "shipping": os.environ.get("SHIPPING")}
    return Response(context, status = 200)

@api_view(['GET'])
def get_cart(request, cart_id):
    cart_items = CartItem.objects.filter(cart_id = cart_id)
    items = CartItemSerializer(cart_items, many = True).data
    context = {"cart_items": items}
    return Response(context, status = 200)

@api_view(['POST'])
def update_cart(request, update_type):
    try:
        data = request.data
        product = Product.objects.get(name = data['product'])
        cart_items = CartItem.objects.filter(cart_id = data['cartId'], product = product)
        if update_type == "add":
            if cart_items:
                cart_item = cart_items[0]
                cart_item.quantity += 1
                cart_item.save()
                return Response({"quantity": cart_item.quantity}, status = 200)
            else:
                cart_item = CartItem.objects.create(cart_id = data['cartId'], product = product, quantity = 1)
            return Response({"quantity": cart_item.quantity}, status = 200)
        elif update_type == "remove":
            if cart_items:
                cart_item = cart_items[0]
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                    return Response({"quantity": cart_item.quantity}, status = 200)
                else:
                    cart_item.delete()
                    return Response({"quantity": 0}, status = 200)
            else:
                raise Exception("Product does not exist in cart.")
        else:
            raise Exception("Invalid method")
    except Exception as e:
        print(e)
        return Response(status = 400)