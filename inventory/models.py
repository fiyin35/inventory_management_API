from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()



# Create your models here.
class Category(models.Model):
    """Product category for better inventory organization"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Supplier(models.Model):
    """Product supplier"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
   

class InventoryItem(models.Model):
    """item model representing products in stock"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, 
                                 on_delete=models.SET_NULL, 
                                 null=True, 
                                 related_name='items')
    supplier = models.ForeignKey(Supplier, 
                                 on_delete=models.SET_NULL, 
                                 null=True, 
                                 related_name='supply_items')
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField(blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Low stock threshold
    LOW_STOCK_THRESHOLD = 10

    def is_low_stock(self):
        """Check if item is low in stock"""
        return self.quantity < self.LOW_STOCK_THRESHOLD
    

    def __str__(self):
        return self.name
    


class StockTransaction(models.Model):

    TRANSACTION_TYPE_CHOICES = [
        ('ADD', 'Stock Added'),
        ('REMOVE', 'Stock Removed'),
    ]

    item = models.ForeignKey(
        InventoryItem, 
        on_delete=models.CASCADE, 
        related_name='stock_transactions'
        )
    
    quantity = models.PositiveIntegerField()
    transaction_type = models.CharField(
        max_length=6, 
        choices=TRANSACTION_TYPE_CHOICES
        )
    timestamp = models.DateTimeField(auto_now_add=True)
    performed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        )
    notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.transaction_type == 'REMOVE':
            # check if there is enough stock to remove
            if self.item.quantity < self.quantity:
                raise ValueError('Not enough stock available')
            self.item.quantity -= self.quantity 
        else:
            self.item.quantity += self.quantity

        self.item.save()
        super().save(*args, **kwargs)
        