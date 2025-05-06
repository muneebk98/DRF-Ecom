from django.shortcuts import render
from django.contrib.auth.models import User
from ecom_app.serializers import UserSerializer, ProductSerializer, OrderItemSerializer,OrderSerializer
from rest_framework import generics, permissions, viewsets, renderers
from ecom_app.models import Product, Order, OrderItem
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, F



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


    
class ProductByUserView(APIView):
    def get(self, request, user_id):
        products = Product.objects.filter(owner__id=user_id)
        
        if not products:
            return Response({"detail": "No products found for this user."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    

class OrderWithTotalQuantityView(APIView):
    def get(self, request, user_id):
    
        orders = Order.objects.filter(user__id=user_id).annotate(total_quantity=Sum('items__quantity'))
        
        if not orders:
            return Response({"detail": "No orders found for this user."}, status=status.HTTP_404_NOT_FOUND)
        
        orders_data = []
        for order in orders:
            order_data = OrderSerializer(order).data
            order_data['total_quantity'] = order.total_quantity  
            orders_data.append(order_data)
        
        return Response(orders_data)
    
class PopularProduct(APIView):
    def get(self,request):
        popular = OrderItem.objects.values('product').annotate(totalquantity=Sum('quantity')).order_by('totalquantity').first()

        product = Product.objects.get(id=popular['product'])
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
class TotalQuantitySold(APIView):
    def get(self,request):
        sold = OrderItem.objects.values('product').annotate(t_quantity=Sum('quantity')).order_by('-t_quantity')

        if not sold:
            return Response({"detail": "No products found."}, status=status.HTTP_404_NOT_FOUND)
        
        data = []

        for item in sold:
            p_id = item['product']
            t_quant = item['t_quantity']

            product = Product.objects.get(id=p_id)

            serializer = ProductSerializer(product)

            product_final = serializer.data
            product_final['quantity_total'] = t_quant

            data.append(product_final)

        return Response(data)

class TotalRevenuePerProductView(APIView):
    def get(self, request):
        
        products_revenue = Product.objects.annotate(
            total_revenue=Sum(F('orderitem__quantity') * F('price')) 
        ).order_by('-total_revenue')  

       
        if not products_revenue:
            return Response({"detail": "No products found."}, status=status.HTTP_404_NOT_FOUND)

      
        product_data = []

       
        for product in products_revenue:
            serializer = ProductSerializer(product)

            product_info = serializer.data
            product_info['total_revenue'] = product.total_revenue 

           
            product_data.append(product_info)

        return Response(product_data)