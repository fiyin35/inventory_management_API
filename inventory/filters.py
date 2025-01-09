from django_filters import rest_framework as filters
from .models import InventoryItem

class InventoryItemFilter(filters.FilterSet):
    min_quantity = filters.NumberFilter(field_name='quantity', lookup_expr='gte')
    max_quantity = filters.NumberFilter(field_name='quantity', lookup_expr='lte')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    category_name = filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    is_low_stock = filters.BooleanFilter(method='filter_low_stock')

    class Meta:
        model = InventoryItem
        fields = {
            'name': ['icontains', 'iexact'],
            'category': ['exact'],
            'created_at': ['date__gte', 'date__lte'],
        }

        def filter_low_stock(self, queryset, name, value):
            if value:
                return queryset.filter(quantity__lte=InventoryItem.LOW_STOCK_THRESHOLD)
            return queryset