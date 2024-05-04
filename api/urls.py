from django.urls import include, path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, PaymentViewSet, CollectViewSet

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(r'users', UserViewSet, 'users')
router_v1.register(r'payments', PaymentViewSet, 'payments')
router_v1.register(r'collects', CollectViewSet, 'collects')

schema_view = get_schema_view(
    openapi.Info(
        title="Donation",
        default_version='v1',
        description="Документация к API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

v1_patterns = [
    path('', include(router_v1.urls)),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path(
        'docs/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
]

urlpatterns = [
    path('v1/', include(v1_patterns)),
]
