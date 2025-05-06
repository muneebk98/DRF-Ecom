from rest_framework import serializers
from ecom_app.models import Product, Order, OrderItem
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Product
        fields = ['id', 'owner', 'title', 'description', 'price', 'stock']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email'] 

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at']


class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.ReadOnlyField(source='product.title')

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'product_title', 'quantity']

    def validate(self, data):
        product = data['product']
        quantity = data['quantity']

        if quantity > product.stock:
            raise serializers.ValidationError(
                f"Only {product.stock} items left in stock."
            )
        return data
