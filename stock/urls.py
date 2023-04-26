from django.urls import path, include
from .views import CategoryView, BrandView, FirmView, ProductView, PurchaseView, SalesView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'categories', CategoryView)
router.register(r'brands', BrandView)
router.register(r'firms', FirmView)
router.register(r'products', ProductView)
router.register(r'purchases', PurchaseView)
router.register(r'sales', SalesView)

urlpatterns = [
]

urlpatterns += router.urls

