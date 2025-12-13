from rest_framework.routers import DefaultRouter

from .views import OrderViewSet

router = DefaultRouter()
router.register(r'sales/orders', OrderViewSet, basename='sales-order')

urlpatterns = router.urls
