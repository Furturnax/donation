from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum, Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    CollectReadSerializer,
    CollectWriteSerializer,
    PaymentReadSerializer,
    PaymentWriteSerializer,
    UserSerializer,
)
from collect.models import Event, User, Payment, Collect


@method_decorator(cache_page(60*30), name='dispatch')
class UserViewSet(DjoserUserViewSet):
    """CRUD пользователей."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = LimitOffsetPagination


@method_decorator(cache_page(60*30), name='dispatch')
class PaymentViewSet(viewsets.ModelViewSet):
    """CRUD платежей."""

    serializer_class = PaymentWriteSerializer
    queryset = Payment.objects.all()
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticated)
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        """Определяет класс сериализатора в зависимости от типа запроса."""
        if self.request.method == 'GET':
            return PaymentReadSerializer
        return PaymentWriteSerializer


@method_decorator(cache_page(60*30), name='dispatch')
class CollectViewSet(viewsets.ModelViewSet):
    """CRUD сборов."""

    queryset = Collect.objects.annotate(
        total_amount=Sum('payments__amount'),
        uniq_patrician=Count('payments__user', distinct=True),
    ).prefetch_related(
        Prefetch(
            'event', queryset=Event.objects.all()
        ),
        Prefetch(
            'payments', queryset=Payment.objects.all().select_related('user')
        ),
    )
    serializer_class = CollectWriteSerializer
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticated)
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        """Определяет класс сериализатора в зависимости от типа запроса."""
        if self.request.method == 'GET':
            return CollectReadSerializer
        return CollectWriteSerializer
