from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from api.views import (
    CategoryViewSet, ProductViewSet,
    ShoppingCartViewSet, SubcategoryViewSet
)

router_v1 = routers.DefaultRouter()
router_v1.register(
    r'categories', CategoryViewSet, basename='categories'
)
router_v1.register(
    r'subcategories', SubcategoryViewSet, basename='subcategories'
)
router_v1.register(
    r'products', ProductViewSet, basename='products'
)
router_v1.register(
    r'shoppingcarts', ShoppingCartViewSet, basename='shoppingcarts'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
