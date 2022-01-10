from django.urls import path
from .views import *

app_name="shop"

urlpatterns = [
    path("cart/",CartView.as_view(),name="cart"),     
    path("promocode/",PromoCodeView.as_view(),name="promocode"),     
    path("address/",AddressView.as_view(),name="address"),     
    path("checkout/",CheckOutView.as_view(),name="checkout"),     
    path("orders/",OrderView.as_view(),name="orders"),     
    path("email/",SendMailView.as_view(),name="email"),     
]

