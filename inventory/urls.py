from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryItemViewSet, CategoryViewSet, SupplierViewSet

router = DefaultRouter()

router.register(r'items', InventoryItemViewSet, basename='inventory')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'suppliers', SupplierViewSet, basename='supplier')


urlpatterns = [
    path('', include(router.urls)),
]