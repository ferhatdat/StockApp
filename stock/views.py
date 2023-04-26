from django.shortcuts import render
from .models import Category, Brand, Firm, Product, Purchases, Sales
from rest_framework.viewsets import ModelViewSet
from .serializers import CategorySerializer, CategoryProductSerializer, BrandSerializer, FirmSerializer, ProductSerializer, PurchasesSerializer, SalesSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import status
from rest_framework.response import Response

class CategoryView(ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['name']
    permission_classes = [DjangoModelPermissions]


    def get_serializer_class(self, *args, **kwargs):
        serializer = super().get_serializer_class(*args, **kwargs)
        if self.request.query_params.get('name'):
            return CategoryProductSerializer
        else:
            return serializer


class BrandView(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class FirmView(ModelViewSet):
    queryset = Firm.objects.all()
    serializer_class = FirmSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['category', 'brand']

class PurchaseView(ModelViewSet):
    queryset = Purchases.objects.all()
    serializer_class = PurchasesSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['firm']
    filterset_fields = ['product', 'firm']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # ADD Product Stock 
        purchase = request.data
        product = Product.objects.get(id=purchase['product_id'])
        product.stock += purchase['quantity']
        product.save()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # UPDATE Product Stock
        purchase = request.data
        product = Product.objects.get(id=instance.product_id)
        difference = purchase['quantity'] - instance.quantity
        print('instance', instance)
        print('purchase', purchase)
        product.stock += difference
        product.save()
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        product = Product.objects.get(id=instance.product_id)
        product.stock -= instance.quantity
        product.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class SalesView(ModelViewSet):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['product']
    filterset_fields = ['brand', 'product']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # ADD Product Stock 
        sales = request.data
        product = Product.objects.get(id=sales['product_id'])
        if product.stock >= sales['quantity']:
            product.stock -= sales['quantity']
            product.save()
        else:
            return Response({'message': f'Dont have enough stock. You have {product.stock} {product.name}'})
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # UPDATE Product Stock
        sales = request.data
        product = Product.objects.get(id=instance.product_id)
        if sales['quantity'] <= product.stock:
            product.stock -= (sales['quantity'] - instance.quantity)
            product.save()
            self.perform_update(serializer)
        else:
            return Response({'message': f'Dont have enough stock. You have {product.stock} {product.name}'})


        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        product = Product.objects.get(id=instance.product_id)
        product.stock += instance.quantity
        product.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)