from django.urls import path
from .views import *

app_name = "base"

urlpatterns = [
    path("",  index, name = ""),
    path("cart-<slug:cart_id>", get_cart, name="get_cart"),
    path("update-cart-<slug:update_type>/", update_cart, name="update_cart"),
    path("checkout/", checkout, name="checkout"),
    path("reg-email/", reg_email, name="reg_email"),
    path("send-message/", send_message, name="send_message")
]