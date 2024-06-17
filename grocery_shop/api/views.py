from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.serializers import (
    CategorySerializer,
    ProductInCartSerializer,
    ProductSerializer,
    ShoppingCartSerializer,
    SubcategorySerializer
)
from shop.models import (
    Category,
    Product,
    ProductInCart,
    ShoppingCart,
    Subcategory
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubcategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ShoppingCartViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_object(self):
        cart, created = ShoppingCart.objects.get_or_create(
            user=self.request.user
        )
        return cart

    @action(detail=False, methods=['post', 'delete'])
    def modify_product(self, request, pk=None):
        cart = self.get_object()
        product = get_object_or_404(Product, pk=pk)
        amount = int(request.data.get('amount', 1))

        if request.method == 'POST':
            product_in_cart, created = ProductInCart.objects.get_or_create(
                cart=cart, products=product, defaults={'amount': amount}
            )
            if not created:
                product_in_cart.amount += amount
                product_in_cart.save()
            serializer = ProductInCartSerializer(product_in_cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            try:
                product_in_cart = ProductInCart.objects.get(
                    cart=cart, products=product
                )
                if product_in_cart.amount > amount:
                    product_in_cart.amount -= amount
                    product_in_cart.save()
                else:
                    product_in_cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except ProductInCart.DoesNotExist:
                return Response(
                    {'error': 'Product not in cart'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            {'error': 'Invalid method'}, status=status.HTTP_400_BAD_REQUEST
        )
