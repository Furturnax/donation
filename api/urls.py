from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, PaymentViewSet, CollectViewSet

app_name = 'api'

router = DefaultRouter()

router.register(r'users', UserViewSet, 'users')
router.register(r'payments', PaymentViewSet, 'payments')
router.register(r'collects', CollectViewSet, 'collects')

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
