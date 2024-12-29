from django.shortcuts import render
from .models import InventoryItem, Category
from .serializers import InvetoryItemSerializer, CategorySerializer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action


class CategoryViewSet(viewsets.ModelViewSet):
    """CRUD operations for product categories"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class InventoryItemViewSet(viewsets.ModelViewSet):
    """CRUD operations for inventory items"""

    queryset = InventoryItem.objects.all()
    serializer_class = InvetoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, serializer):
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
