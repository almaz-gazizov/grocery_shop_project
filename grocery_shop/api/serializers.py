from rest_framework import serializers

from shop.models import (
    Category,
    Product,
    ProductInCart,
    ShoppingCart,
    Subcategory
)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class SubcategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Subcategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ProductInCartSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(
        max_digits=8, decimal_places=2, read_only=True
    )

    class Meta:
        model = ProductInCart
        fields = '__all__'


class ShoppingCartSerializer(serializers.ModelSerializer):
    products = ProductInCartSerializer(
        many=True, read_only=True, source='cartproducts'
    )
    total_price = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCart
        fields = ['user', 'products', 'total_price', 'total_quantity']

    def get_total_price(self, obj):
        return sum(item.total_price for item in obj.cartproducts.all())

    def get_total_quantity(self, obj):
        return sum(item.quantity for item in obj.cartproducts.all())
