from decimal import Decimal

from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from collect.models import Collect, Event, Payment
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя."""

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
        )
        ref_name = 'CustomUser'


class UserShortSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода имени и фамилии пользователя."""

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'full_name',
        )

    def get_full_name(self, obj):
        """Возвращает имя и фамилию."""
        if obj.first_name or obj.last_name:
            return f'{obj.first_name} {obj.last_name}'
        return obj.username


class EventSerializer(serializers.ModelSerializer):
    """Сериализатор модели события."""

    class Meta:
        model = Event
        fields = (
            'title',
        )


class PaymentWriteSerializer(serializers.ModelSerializer):
    """Сериализатор модели платежа."""

    class Meta:
        model = Payment
        fields = (
            'id',
            'collect',
            'user',
            'amount',
            'created_at',
        )

    @transaction.atomic
    def create(self, validated_data):
        """Метод для создания платежа."""
        payment = Payment.objects.create(**validated_data)
        payment.save()
        send_mail(
            'Платёж создан',
            'Ваш платеж успешно создан!',
            'support@dotations.com',
            [self.context['request'].user.email],
            fail_silently=True,
        )
        return payment


class PaymentReadSerializer(serializers.ModelSerializer):
    """Сериализатор модели платежа."""

    user = UserShortSerializer()

    class Meta:
        model = Payment
        fields = (
            'id',
            'collect',
            'user',
            'amount',
            'created_at',
        )


class PaymentSortSerializer(serializers.ModelSerializer):
    """Сериализатор модели платежа."""

    user = UserShortSerializer()

    class Meta:
        model = Payment
        fields = (
            'user',
            'amount',
            'created_at',
        )


class CollectReadSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации о сборе."""

    author = UserShortSerializer()
    event = EventSerializer(many=True)
    current_amount = serializers.SerializerMethodField()
    patrician_count = serializers.SerializerMethodField()
    list_payments = serializers.SerializerMethodField()

    class Meta:
        model = Collect
        fields = (
            'id',
            'author',
            'title',
            'event',
            'text',
            'target_amount',
            'current_amount',
            'patrician_count',
            'cover',
            'endtime',
            'created_at',
            'list_payments',
        )

    def get_current_amount(self, obj):
        """Метод для получения собранной суммы."""
        return obj.payments.aggregate(
            current_amount=Sum('amount')
        )['current_amount'] or Decimal('0.00')

    def get_patrician_count(self, obj):
        """Метод для получения количества патриций."""
        return obj.payments.values('user').distinct().count()

    def get_list_payments(self, obj):
        """Метод для получения списка платежей."""
        return PaymentSortSerializer(obj.payments.all(), many=True).data


class CollectWriteSerializer(serializers.ModelSerializer):
    """Сериализатор создания сбора."""

    event = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(),
        many=True,
    )
    cover = Base64ImageField(
        allow_null=False,
        allow_empty_file=False,
    )

    class Meta:
        model = Collect
        fields = (
            'author',
            'title',
            'event',
            'text',
            'target_amount',
            'cover',
            'endtime',
        )

    @transaction.atomic
    def create(self, validated_data):
        """Метод для создания сбора."""
        events_data = validated_data.pop('event')
        collect = Collect.objects.create(**validated_data)
        for event_data in events_data:
            collect.event.add(event_data)
        collect.save()
        send_mail(
            'Сбор создан',
            'Ваш сбор успешно создан!',
            'support@dotations.com',
            [self.context['request'].user.email],
            fail_silently=True,
        )
        return collect

    def validate_endtime(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                'Дата окончания должна быть больше текущей.'
            )
        return value

    def to_representation(self, instance):
        """Метод для представления сбора."""
        return CollectReadSerializer(
            instance,
            context=self.context,
        ).data
