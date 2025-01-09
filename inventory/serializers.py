from rest_framework import serializers
from .models import Category, Supplier, InventoryItem, StockTransaction


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class SupplierSerializer(serializers.ModelSerializer):
    """Serializer for the Supplier model"""
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'description']


class InventoryItemSerializer(serializers.ModelSerializer):
    """serializer for inventory item model"""

    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    supplier = SupplierSerializer(read_only=True)
    supplier_id = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(),
        source='supplier',
        write_only=True
    )
    is_low_stock = serializers.ReadOnlyField()

    class Meta:
        model = InventoryItem
        fields = [
            'id',
            'name',
            'description',
            'category',
            'category_id',
            'supplier',
            'supplier_id',
            'quantity',
            'expiry_date',
            'price',
            'created_by',
            'created_at',
            'updated_at',
            'is_low_stock'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']
    
    def get_is_low_stock(self, obj):
        return obj.is_low_stock()
    

class StockTransactionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = StockTransaction 
        fields = ['id', 'item', 'quantity', 'transaction_type', 'timestamp', 'notes']
        read_only_fields = ['timestamp']




