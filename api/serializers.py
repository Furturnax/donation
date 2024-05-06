import os

from django.core.mail import send_mail
from django.utils import timezone
from dotenv import load_dotenv
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from collect.models import Collect, Event, Payment
from core.consts import DECIMAL_PLACE, MAX_DIGITS_IN_DECIMAL
from users.models import User

load_dotenv(
    dotenv_path='./docker/envfiles/.env'
)


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
    """Сериализатор сокращенной модели пользователя."""

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
        )


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

    def create(self, validated_data):
        """Метод для создания платежа."""
        payment = Payment.objects.create(**validated_data)
        payment.save()
        send_mail(
            'Платёж создан',
            'Ваш платеж успешно создан!',
            os.getenv('EMAIL_HOST_USER'),
            [self.context['request'].user.email],
            fail_silently=True,
        )
        return payment


class PaymentReadSerializer(serializers.ModelSerializer):
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


class PaymentShortSerializer(serializers.ModelSerializer):
    """Сериализатор модели платежа."""

    user = UserShortSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = (
            'user',
            'amount',
            'created_at',
        )


class CollectReadSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации о сборе."""

    author = UserShortSerializer(source='user', read_only=True)
    event = EventSerializer(many=True, read_only=True)
    current_amount = serializers.DecimalField(
        source='total_amount',
        max_digits=MAX_DIGITS_IN_DECIMAL,
        decimal_places=DECIMAL_PLACE,
        read_only=True
    )
    patrician_count = serializers.IntegerField(
        source='uniq_patrician', read_only=True
    )
    list_payments = PaymentShortSerializer(
        source='payments', many=True, read_only=True
    )

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
            os.getenv('EMAIL_HOST_USER'),
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
