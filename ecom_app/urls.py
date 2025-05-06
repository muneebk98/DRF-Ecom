from django.urls import path, include
from .views import ProductByUserView
from rest_framework.routers import DefaultRouter
from ecom_app.views import (
    UserViewSet,
    ProductViewSet,
    OrderViewSet,
    OrderItemViewSet,
    OrderWithTotalQuantityView,
    PopularProduct,
    TotalQuantitySold,
    TotalRevenuePerProductView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='orderitem')

urlpatterns = [
    path('', include(router.urls)),
    path('products/user/<int:user_id>/', ProductByUserView.as_view(), name='product-by-user'),
    path('orders/user/<int:user_id>/total-quantity/', OrderWithTotalQuantityView.as_view(), name='order-with-total-quantity'),
    path('products/mostpop',PopularProduct.as_view(),name='most-popular'),
    path('products/mostsold',TotalQuantitySold.as_view(),name='totalquantitysold'),
     path('products/mostrevenue/', TotalRevenuePerProductView.as_view(), name='most-revenue-products'),
]