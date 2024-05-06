from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum, Prefetch

from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    CollectReadSerializer,
    CollectWriteSerializer,
    PaymentReadSerializer,
    PaymentWriteSerializer,
    UserSerializer,
)
from collect.models import Event, User, Payment, Collect


class UserViewSet(DjoserUserViewSet):
    """Вьюсет для работы с пользователями."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = LimitOffsetPagination


class PaymentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с платяжом."""

    serializer_class = PaymentWriteSerializer
    queryset = Payment.objects.all()
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticated)
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        """Определяет класс сериализатора в зависимости от типа запроса."""
        if self.request.method == 'GET':
            return PaymentReadSerializer
        return PaymentWriteSerializer


class CollectViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы со сбором."""

    queryset = Collect.objects.annotate(
        total_amount=Sum('payments__amount'),
        uniq_patrician=Count('payments__user', distinct=True),
    ).prefetch_related(
        Prefetch(
            'event', queryset=Event.objects.all()
        ),
        Prefetch(
            'payments', queryset=Payment.objects.select_related('user').all()
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
