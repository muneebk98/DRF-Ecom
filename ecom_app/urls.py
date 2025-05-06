from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ecom_app.views import (
    UserViewSet,
    ProductViewSet,
    OrderViewSet,
    OrderItemViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='orderitem')

urlpatterns = [
    path('', include(router.urls)),
]