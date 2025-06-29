from django.urls import path

# from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from . import views


router = routers.DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('categories', views.CategoryViewSet)
router.register('carts', views.CartViewSet)

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('images', views.ProductImageViewSet, basename='product-images')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = [
    path('order/', views.place_order),
    path('payment/success', views.payment_success, name='payment_success'),
    path('payment/cancel', views.payment_cancel),
]

urlpatterns += router.urls + carts_router.urls + products_router.urls