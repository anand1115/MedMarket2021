from django.urls import path
from .views import *

app_name="product"

urlpatterns = [
    path("category/",CategoryView.as_view(),name="category"),    
    path("subcategory/",SubCategoryView.as_view(),name="subcategory"),    
    path("brand/",BrandView.as_view(),name="brand"),    
    path("product/",ProductView.as_view(),name="product"),    
    path("product_list/",ProductListView.as_view(),name="product"),    
]

