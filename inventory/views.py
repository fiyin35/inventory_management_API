from .models import InventoryItem, Category, StockTransaction
from .serializers import InventoryItemSerializer, CategorySerializer, StockTransactionSerializer
from .pagination import StandardResultsPagination

from .filters import InventoryItemFilter
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from decimal import Decimal
from django.core.exceptions import ValidationError


class CategoryViewSet(viewsets.ModelViewSet):
    """CRUD operations for product categories"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class InventoryItemViewSet(viewsets.ModelViewSet):
    """CRUD operations for inventory items"""

    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    pagination_class = StandardResultsPagination
    permission_classes = [permissions.IsAuthenticated]

    filterset_class = InventoryItemFilter
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['name', 'price', 'quantity', 'created_at']
    ordering = ['name']

    def get_queryset(self):
        queryset = InventoryItem.objects.all()
        if self.action == 'list':
            return queryset.select_related('category', 'created_by')
        return queryset

    def perform_create(self, serializer):
        """Automatically set the created_by to current logged in user"""

        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['GET'])
    def low_stock_items(self, request):
        """Endpoint to retrieve items with low stock"""

        low_stock_items = self.queryset.filter(
            quantity__lte=InventoryItem.LOW_STOCK_THRESHOLD
        )
        serializer = self.get_serializer(low_stock_items, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['PATCH'])
    def update_quantity(self, request, pk=None):
        """update item quantity"""

        item = self.get_object()
        quantity = request.data.get('quantity')

        if quantity is not None:
            item.quantity = quantity
            item.save()
            serializer = self.get_serializer(item)
            return Response(serializer.data)
        
        return Response(
            {'error': 'Quantity must be provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['PATCH'])
    def add_stock(self, request, pk=None):
        """Add stock to inventory item"""

        return self._handle_stock_change(request, 'ADD')
    
    @action(detail=True, methods=['PATCH'])
    def reduce_stock(self, request, pk=None):
        """Remove stock from inventory item"""

        return self._handle_stock_change(request, 'REMOVE')
    
    @action(detail=True, methods=['GET'])
    def stock_level(self, request, pk=None):
        """Get current stock level and recent transaction"""
        item = self.get_object()
        recent_transactions = item.stock_transactions.order_by('-timestamp')[:5]

        data = {
            'current_stock': item.quantity,
            'is_low_stock': item.is_low_stock(),
            'recent_transactions': StockTransactionSerializer(
                recent_transactions,
                many=True
            ).data
        }
        return Response(data)
    
    def _handle_stock_change(self, request, transaction_type):
        """Helper method to handle stock changes"""
        item = self.get_object()
        quantity = request.data.get('quantity')
        notes = request.data.get('notes', '')

        if not quantity or not isinstance(quantity, (int, float, Decimal)):
            return Response(
                {'error': 'Valid quantity required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            transaction = StockTransaction.objects.create(
                item=item,
                quantity=quantity,
                transaction_type=transaction_type,
                performed_by=request.user,
                notes=notes 
            )

            return Response({
                'message': f'Stock successfully {"added" if transaction_type == "ADD" else "reduced"}',
                'current_stock': item.quantity,
                'transaction': StockTransactionSerializer(transaction).data
            })
        
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    
