from rest_framework import serializers
from .models import Category, Brand, Firm, Product, Purchases, Sales
import datetime

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    category_id = serializers.IntegerField()
    brand = serializers.StringRelatedField()
    brand_id = serializers.IntegerField()
    class Meta:
        model = Product
        fields = ('name', 'category_id', 'category', 'brand_id', 'brand', 'stock')
        read_only_fields=('stock', )

class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ('id', 'name', 'product_count')

    def get_product_count(self, obj):
        # return obj.products.count()
        return Product.objects.filter(category=obj).count()
    
class CategoryProductSerializer(serializers.ModelSerializer):

    product_count = serializers.SerializerMethodField()
    products = ProductSerializer(many=True)
    class Meta:
        model = Category
        fields = ('id', 'name', 'product_count', 'products')

    def get_product_count(self, obj):
        # return obj.products.count()
        return Product.objects.filter(category=obj).count()


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name', 'image')

class FirmSerializer(serializers.ModelSerializer):

    class Meta:
        model = Firm
        fields = ('id', 'name', 'phone', 'image', 'address')

class PurchasesSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    firm = serializers.StringRelatedField()
    firm_id = serializers.IntegerField()
    brand = serializers.StringRelatedField()
    brand_id = serializers.IntegerField()
    product = serializers.StringRelatedField()
    product_id = serializers.IntegerField()
    category = serializers.SerializerMethodField()
    time_hour = serializers.SerializerMethodField()
    createds = serializers.SerializerMethodField()

    class Meta:
        model = Purchases
        fields = ('id', 'user', 'user_id', 'firm', 'firm_id', 'brand', 'brand_id', 'product', 'product_id', 'quantity', 'price', 'price_total', 'updated', 'category', 'time_hour', 'createds')

    def get_category(self, obj):
        return obj.product.category.name
    
    def get_time_hour(self, obj):
        # return obj.createds.strftime("%H:%M")
        return datetime.datetime.strftime(obj.createds, "%H:%M")
    
    def get_createds(self, obj):
        return obj.updated.strftime("%d,%m,%Y")
        # return datetime.datetime.strftime(obj.updated, "%d,%m,%Y")

class SalesSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    brand_id = serializers.IntegerField()
    product = serializers.StringRelatedField()
    product_id = serializers.IntegerField()
    category = serializers.SerializerMethodField()
    time_hour = serializers.SerializerMethodField()
    createds = serializers.SerializerMethodField()

    class Meta:
        model = Sales
        fields = ('id', 'user', 'user_id', 'brand', 'brand_id', 'product', 'product_id', 'quantity', 'price', 'price_total', 'updated', 'category', 'time_hour', 'createds')

    def get_category(self, obj):
        return obj.product.category.name
    
    def get_time_hour(self, obj):
        # return obj.createds.strftime("%H:%M")
        return datetime.datetime.strftime(obj.createds, "%H:%M")
    
    def get_createds(self, obj):
        return obj.updated.strftime("%d,%m,%Y")
        # return datetime.datetime.strftime(obj.updated, "%d,%m,%Y")

