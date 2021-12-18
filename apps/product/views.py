import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import pagination, filters


from .models import *
from .serializers import *

class CategoryView(APIView):

    def get(self,request):
        category_id=request.GET.get("id")
        if(category_id):
            try:
                category=Category.objects.get(id=category_id,active=True)
                return Response({"data":CategorySerializer(category).data})
            except:
                return Response({"error":"Category Doesn't Exit"},400)
        else:
            categories=Category.objects.filter(active=True)     
            return Response({"data":CategorySerializer(categories,many=True).data},200)


class SubCategoryView(APIView):

    def get(self,request):
        subcategory_id=request.GET.get("id")
        if(subcategory_id):
            try:
                subcategory=SubCategory.objects.get(id=subcategory_id,active=True)
                return Response({"data":SubCategorySerializer(subcategory).data})
            except:
                return Response({"error":"SubCategory Doesn't Exit"},400)
        else:
            subcategories=SubCategory.objects.filter(active=True)        
            return Response({"data":SubCategorySerializer(subcategories,many=True).data},200)

class BrandView(APIView):

    def get(self,request):
        brand_id=request.GET.get("id")
        if(brand_id):
            try:
                brand=Brand.objects.get(id=brand_id,active=True)
                return Response({"data":BrandSerializer(brand).data})
            except:
                return Response({"error":"brand Doesn't Exit"},400)
        else:
            brands=Brand.objects.filter(active=True)        
            return Response({"data":BrandSerializer(brands,many=True).data},200)



class ProductView(APIView):

    def get(self,request):
        data=request.GET 
        id=data.get("id")
        if not id: 
            return Response({"error":"Product id doesn't exist !!"},400)
        try:
            product=Product.objects.get(id=id)
        except:
            return Response({"error":"Product Doesn't exist with this id !!"},400)
        return Response({"data":ProductSerializer(product).data},200)


class MyPagination(pagination.PageNumberPagination):

	page_size = 10
	page_size_query_param = 'page_size'
	max_page_size = 100
	def get_paginated_response(self, data):
		return Response({
        	'status':True,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total_products_count': self.page.paginator.count,
            'total_pages_count': self.page.paginator.num_pages,
			'current_page_count':len(self.page),
			'start_product_index':self.page.start_index(),
			'end_product_index':self.page.end_index(),
            'data': data
        })


class PriceRangeFilter(django_filters.FilterSet):

	selling_price=django_filters.RangeFilter()
	category=django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all(),to_field_name='id')
	subcategory=django_filters.ModelMultipleChoiceFilter(queryset=SubCategory.objects.all(),to_field_name='id')

	class Meta:
		model=Product
		fields=['selling_price','category','subcategory']

class ProductListView(APIView,MyPagination):

	serializer_class=ProductSerializer
	pagination_class=MyPagination
	filter_backends = [filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend]
	search_fields=['title','category__title',"subcategory__title"]
	ordering_fields=['selling_price','discount','title']
	filter_class=PriceRangeFilter

	def get(self,request):
		data=self.filter_queryset(self.get_queryset())			
		result=self.paginate_queryset(data, request, view=self)
		serializer=self.serializer_class(result,many=True)
		return self.get_paginated_response(serializer.data)
	
	def filter_queryset(self, queryset):        
		for backend in list(self.filter_backends):
			queryset = backend().filter_queryset(self.request, queryset, self)
		return queryset

	def get_queryset(self):
		return Product.objects.filter(active=True)


