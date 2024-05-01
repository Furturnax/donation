from django.db import transaction
from django.db.models import Count
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


class UserShortSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода имени и фамилии пользователя."""

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
        )


class EventSerializer(serializers.ModelSerializer):
    """Сериализатор модели события."""

    class Meta:
        model = Event
        fields = (
            'id',
            'title',
        )


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор модели платяжа."""

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
        collect = validated_data.get('collect')
        amount = validated_data.get('amount')
        payment = Payment.objects.create(**validated_data)
        collect.current_amount += amount
        patricians_count = (
            Payment.objects.filter(collect=collect)
            .values('user')
            .annotate(total=Count('user'))
            .count()
        )
        collect.patrician_count = patricians_count
        collect.save()
        return payment


class PaymentShortSerializer(serializers.ModelSerializer):
    """Короткий сериализатор модели платежа."""

    user = UserShortSerializer()

    class Meta:
        model = Payment
        fields = (
            'id',
            'user',
            'amount',
            'created_at',
        )


class CollectReadSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации о сборе."""

    author = UserSerializer(read_only=True)
    event = EventSerializer(many=True, read_only=True)
    list_payment = serializers.SerializerMethodField()

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
            'list_payment',
        )

    def get_list_payment(self, obj):
        """Метод для получения списка платежей."""
        payments = Payment.objects.filter(collect=obj)
        return PaymentShortSerializer(payments, many=True).data


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
        cover_image_data = validated_data.pop('cover')
        collect = Collect.objects.create(**validated_data)
        for event_data in events_data:
            collect.event.add(event_data)
        collect.cover = cover_image_data
        collect.save()
        return collect

    def to_representation(self, instance):
        """Метод для представления сбора."""
        return CollectReadSerializer(
            instance,
            context=self.context,
        ).data
