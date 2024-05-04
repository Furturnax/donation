import random

from django.core.management.base import BaseCommand
from django.utils import timezone
from mimesis import Generic

from collect.models import Collect, Event, Payment
from users.models import User

MIN_EVENTS = 1
MAX_EVENTS = 2
MIN_PAYMENTS = 1
MAX_PAYMENTS = 3
MIN_USERS = 1
MAX_USERS = 3


class Command(BaseCommand):
    help = 'Наполнение базы данных синтетическими данными.'

    def handle(self, *args, **kwargs):
        generic = Generic('ru')

        users = [
            User(
                email=generic.person.email(),
                username=generic.person.username(),
                first_name=generic.person.name(),
                last_name=generic.person.surname(),
            ) for _ in range(100)
        ]
        User.objects.bulk_create(users)
        self.stdout.write(
            self.style.SUCCESS('Создано {} пользователей'.format(len(users)))
        )

        events = [Event(title=generic.text.word()) for _ in range(50)]
        Event.objects.bulk_create(events)
        self.stdout.write(
            self.style.SUCCESS('Создано {} событий'.format(len(events)))
        )

        collects = []
        for _ in range(3000):
            author = generic.choice(users)
            collect = Collect(
                author=author,
                title=generic.text.title(),
                # event у меня не получилось привязать, слишком много времени
                # запись добавлялась в бд
                text=generic.text.text(),
                target_amount=generic.numeric.integer_number(
                    start=100,
                    end=10000
                ),
                endtime=timezone.make_aware(
                    generic.datetime.datetime(start=2025, end=2030),
                    timezone.get_current_timezone()
                )
            )
            collects.append(collect)
        Collect.objects.bulk_create(collects)
        self.stdout.write(
            self.style.SUCCESS('Создано {} сборов'.format(len(collects)))
        )

        payments = []
        for collect in collects:
            num_payments = random.randint(MIN_PAYMENTS, MAX_PAYMENTS)
            num_users = random.randint(MIN_USERS, min(MAX_USERS, len(users)))

            unique_users = random.sample(users, num_users)

            for _ in range(num_payments):
                for user in unique_users:
                    payment = Payment(
                        collect=collect,
                        user=user,
                        amount=generic.numeric.integer_number(
                            start=1,
                            end=1000
                        ),
                    )
                    payments.append(payment)
        Payment.objects.bulk_create(payments)
        self.stdout.write(
            self.style.SUCCESS('Создано {} платежей'.format(len(payments)))
        )

        self.stdout.write(
            self.style.SUCCESS('Успешное завершение наполнения базы данных.')
        )
