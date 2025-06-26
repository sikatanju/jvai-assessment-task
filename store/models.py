from django.db import models
from django.core.validators import MinValueValidator

from uuid import uuid4

from core.models import UserProfile

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    unit_price = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    inventory = models.PositiveIntegerField()
    last_update = models.DateTimeField(auto_now=True)
    # category is used to categorized products.
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='products')
    
    def __str__(self) -> str:
        return self.title



class Cart(models.Model):
    # The Cart isn't tied to any specific user, so that an anonymous user can also add products to their cart...
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    # CartItem simply stores all the products with specified quantity of a cart.
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        # One Cart can only contain a product at most once, the quantity is used to specify how many of that product is ordered 
        unique_together = [['cart', 'product']]


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    placed_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    total_amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])


class ProductImage(models.Model):
    image_url = models.URLField(blank=True, null=True)  
    public_id = models.CharField(max_length=255, blank=True, null=True)  
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    created_at = models.DateTimeField(auto_now_add=True)