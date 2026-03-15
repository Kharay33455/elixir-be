from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
import os
from .basefuncs import validate_checkout_data, create_order
from django.contrib.auth.models import User
from django.core.validators import validate_email

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
    except Exception:
        return Response(status = 400)

@api_view(['POST'])
def checkout(request):
    try:
        is_valid = validate_checkout_data(request.data)
        if is_valid != "Data valid":
            return Response({"err": is_valid}, status = 400)
        cart = request.headers['Authorization']
        try:
            order_id = create_order(request.data, cart)
        except Exception as e:
            return Response({"err":str(e)}, status = 400)
        return Response({"order_id": order_id}, status = 200)
    except Exception as e:
        return Response({"err": "Order creation failed."}, status = 400)

@api_view(['POST'])
def reg_email(request):
    try:
        data = request.data
        try:
            validate_email(data['email'])
        except Exception as e:
            err = list(e)
            return Response({"err": err[0]}, status = 400)
        is_reg = User.objects.filter(username = data['email'], email = data['email'])
        if is_reg:
            return Response({"msg":"Email already registered."}, status = 200)
        User.objects.create_user(username = data['email'], email = data['email'], password = None)
        return Response({'msg':"Email registered."})
    except Exception as e:
        return Response({"err":"Email registration failed."}, status = 400)


@api_view(['POST'])
def send_message(request):
    data = request.data
    try:
        try:
            if str(data['message']).strip() == "":
                raise Exception("Message cannot be empty")
            if str(data['sender']).strip() == "":
                raise Exception("Enter your name to continue.")
        except Exception as e:
            return Response({"err": str(e)}, status = 400)
        
        try:
            validate_email(data['email'])
        except Exception as e:
            return Response({"err": list(e)[0]}, status = 400)
        existing = Message.objects.filter(message_sender = data['sender'],
                               email = data['email'],
                               message = data['message'])
        if existing:
            return Response({"err":"Duplicate message"}, status = 400)
        
        Message.objects.create(message_sender = data['sender'],
                               email = data['email'],
                               message = data['message'])
        return Response(status = 200)
    except Exception as e:
        print(e)
        return Response({"err":"Message sending failed."}, status  = 400)