from django.shortcuts import render
from django.contrib.auth.models import User
from ecom_app.serializers import UserSerializer, ProductSerializer, OrderItemSerializer,OrderSerializer
from rest_framework import generics, permissions, viewsets, renderers
from ecom_app.models import Product, Order, OrderItem
from rest_framework.exceptions import ValidationError


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class OrderViewSet(viewsets.ModelViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        order_item = serializer.save()
        product = order_item.product

        if order_item.quantity > product.stock:
            raise ValidationError(f"Only {product.stock} items in stock.")

        product.stock -= order_item.quantity
        product.save()