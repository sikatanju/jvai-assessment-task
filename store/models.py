from django.db import models

# Create your models here.
class Cateogry(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    unit_price = models.PositiveIntegerField()
    inventory = models.PositiveIntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(
        Cateogry, on_delete=models.PROTECT, related_name='products')
    
    def __str__(self) -> str:
        return self.title
