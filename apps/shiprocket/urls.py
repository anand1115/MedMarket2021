from django.urls import path
from .views import *

app_name="shiprocket"

urlpatterns = [
    path("check_courier/",CheckCourier.as_view(),name="check"),
]

