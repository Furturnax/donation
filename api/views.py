from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    CollectReadSerializer,
    CollectWriteSerializer,
    PaymentReadSerializer,
    PaymentWriteSerializer,
    UserSerializer,
)
from collect.models import User, Payment, Collect


class UserViewSet(DjoserUserViewSet):
    """Вьюсет для работы с пользователями."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = LimitOffsetPagination


class PaymentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с платяжом."""

    serializer_class = PaymentWriteSerializer
    queryset = Payment.objects.all()
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        """Определяет класс сериализатора в зависимости от типа запроса."""
        if self.request.method == 'GET':
            return PaymentReadSerializer
        return PaymentWriteSerializer


class CollectViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы со сбором."""

    serializer_class = CollectWriteSerializer
    queryset = Collect.objects.all()
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        """Определяет класс сериализатора в зависимости от типа запроса."""
        if self.request.method == 'GET':
            return CollectReadSerializer
        return CollectWriteSerializer
