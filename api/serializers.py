from django.utils import timezone
from dotenv import load_dotenv
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from api.tasks import send_collect_created_email, send_payment_created_email
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
        payment = super().create(validated_data)
        send_payment_created_email.delay_on_commit(payment.id)
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
        collect = super().create(validated_data)
        send_collect_created_email.delay_on_commit(collect.id)
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
