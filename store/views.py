from django.shortcuts import render

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter 
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .filters import ProductFilter
from .pagination import ProductPagination
from .permissions import IsAdminOrReadOnly

# Create your views here.
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    pagination_class = ProductPagination
    search_fields = ['title', 'description']

    def get_serializer_context(self):
        return {'request': self.request}