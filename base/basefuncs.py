import phonenumbers
from django.core.validators import validate_email
from .models import CartItem, OrderItem, Order
import random
import string
import os

def validate_checkout_data(data):
    # name: "",
    #     email: "",
    #     phone: "",
    #     address: "",
    #     city: "",
    #     state: "",
    NIGERIAN_STATES = [
    "Outside Nigeria",
    "Abia",
    "Adamawa",
    "Akwa Ibom",
    "Anambra",
    "Bauchi",
    "Bayelsa",
    "Benue",
    "Borno",
    "Cross River",
    "Delta",
    "Ebonyi",
    "Edo",
    "Ekiti",
    "Enugu",
    "FCT",
    "Gombe",
    "Imo",
    "Jigawa",
    "Kaduna",
    "Kano",
    "Katsina",
    "Kebbi",
    "Kogi",
    "Kwara",
    "Lagos",
    "Nasarawa",
    "Niger",
    "Ogun",
    "Ondo",
    "Osun",
    "Oyo",
    "Plateau",
    "Rivers",
    "Sokoto",
    "Taraba",
    "Yobe",
    "Zamfara"]
    if "data:image/" not in str(data['receipt']).strip().split(",")[0]:
        return "Upload a receipt image."
    if str(data['form']['name']).strip() == "":
        return "Provide name to continue"
    if len(str(data['form']['address']).strip()) < 10:
        return "Invalid address. Enter full address."
    if len(str(data['form']['city']).strip()) < 3:
        return "Enter your city in full."
    if str(data['form']['state']).strip() not in NIGERIAN_STATES:
        return "Invalid State."
    try:
        phone_number = phonenumbers.parse(str(data['form']['phone']).strip())
        if not phonenumbers.is_valid_number(phone_number):
            return "Invalid phone number."
    except:
        return "Invalid phone number"
    try:
        validate_email(str(data['form']['email']).strip())
    except:
        return "Invalid email."
    return "Data valid"
    


def create_order(data, cart):
    cart_items = CartItem.objects.filter(cart_id = cart)
    if len(cart_items) < 1:
        raise Exception("Empty order. Start shopping now!")
    alpha = list(string.ascii_letters + string.digits)
    order_id = "".join(random.choice(alpha) for _ in range(100))
    total = 0.0
    order = Order.objects.create(order_id = order_id,
                                 total = total,
                                 name = data['form']['name'],
                                 address = data['form']['address'],
                                 city = data['form']['city'],
                                 state = data['form']['state'],
                                 email = data['form']['email'],
                                 phone_number = data['form']['phone'],
                                 receipt = data['receipt'])
    for item in cart_items:
        OrderItem.objects.create(
            product_name = item.product.name,
            quantity = item.quantity,
            unit_price = item.product.price,
            order = order)
        total += float(item.product.price) * float(item.quantity)
    total += float(os.environ.get("SHIPPING"))
    order.total = total
    order.save()
    return order_id