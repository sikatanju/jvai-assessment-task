from jvai.settings import STRIPE_API_KEY

import stripe

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter 
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Category, Cart, CartItem, Order, ProductImage, Review
from core.models import UserProfile
from .filters import ProductFilter
from .pagination import ProductPagination
from .permissions import IsAdminOrReadOnly
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer, \
    ProductImageSerializer, CreateProductImageSerializer, ReviewSerializer

stripe.api_key=STRIPE_API_KEY

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


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):
    if str(request.user) != 'AnonymousUser':
        cart_id = request.data.get('cart_id', '')
        try:
            cart= Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist():
            return Response({"error": "Cart Does not exists"}, status=status.HTTP_400_BAD_REQUEST)

        if cart.items.count() == 0:
            return Response({"message": "No item in the cart, kindly add at least one item to place an order."}, status=status.HTTP_400_BAD_REQUEST)

        customer = UserProfile.objects.get(user=request.user)
        cart_items = cart.items.all()
        total_price = sum([item.quantity * item.product.unit_price for item in cart_items])
        order = Order.objects.create(customer=customer, total_amount=total_price)
        try:
            session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(total_price*100),
                        'product_data': {
                            'name': f'Order_ID: {order.id}'
                        }
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=f'http://localhost:8000/store/payment/success?order_id={order.id}&cart_id={cart_id}',
                cancel_url=f'http://localhost:8000/store/payment/cancel?order_id={order.id}'
            )
        except Exception as e:
            print(str(e))
            return Response({'error': "Exception occurred"}, status=status.HTTP_400_BAD_REQUEST)
        data = { 'stripe_session': session.url }
        return Response({'stripe': data})
    else:
        return Response({'error': "Please provide authentication credentials."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def payment_success(request):
    order_id = request.GET.get('order_id')
    cart_id = request.GET.get('cart_id')
    
    # Delete all the items from the cart...
    CartItem.objects.filter(cart=cart_id).delete()
    
    # Update Order payment status
    order = Order.objects.get(id=order_id)
    order.payment_status = order.PAYMENT_STATUS_COMPLETE
    order.save()
    
    return Response({"message": f"Payment successful for Order no. {order_id}"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def payment_cancel(request):
    # Update Order payment status
    order_id = request.GET.get('order_id')
    order = Order.objects.get(id=order_id)
    order.payment_status = order.PAYMENT_STATUS_FAILED
    order.save()

    #Currently no retrying to pay for an order exists...
    return Response({"message": "Payment Cancelled for order no.{order_id}"})


class ProductImageViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateProductImageSerializer
        
        return ProductImageSerializer

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}