# Проект "Donation"

Реализация веб-сервиса на базе `Django`, предоставляющий `CRUD REST API` для групповых денежных сборов.

### Требования

1. Данные хранятся в реляционной БД, взаимодействие с ней осуществляется посредством `Django ORM`.
2. `API` реализовано на базе `Django REST Framework`.
3. Реализовано кэширование данных, возвращаемых `GET` эндпоинтом, с обеспечением достоверности ответов.
4. Проект должен быть докеризирован и запускаться через `docker compose up`.
5. Должна присутствовать `Management command` для наполнения БД моковыми данными (несколько тысяч).
6. При создании Группового сбора или Платежа по сбору на почту автора/ донатера должно прийти письмо с информацией об успешном создании сбора (отправке платежа).
7. Все эндпоинты соответствуют `REST` и покрыты документацией `Swagger`.

<br>

## Технологический стек:
- [Python 3.11.5](https://docs.python.org/release/3.11.5/)
- [Django 3.2.23](https://docs.djangoproject.com/en/3.2.23/)
- [Django REST Framework 3.12.4](https://www.django-rest-framework.org/topics/documenting-your-api/)
- [Python dotenv 1.0.1](https://pypi.org/project/python-dotenv/)
- [Mimesis 16.0.0](https://pypi.org/project/mimesis/)
- [Redis 5.0.4](https://pypi.org/project/redis/)
- [Celery 5.4.0](https://pypi.org/project/celery/)

<br>

## Запуск проекта :shipit: :
[Руководство по созданию переменных окружения](./docker/envfiles/.env.example)

[Руководство по развёртыванию проекта локально](./SetUpLocal.md)

<br>

## Порядок запросов к API

http://localhost:8000/api/v1/ - Основной ресурс.

http://localhost:8000/api/v1/docs/ - Документация.

/users/ - Пользователи.

/payments/ - Платежи.

/collects/ - Сборы.

http://localhost:8000/api/v1/users/ - Регистрация.

http://localhost:8000/api/v1/auth/token/login/ - Получение токена.

`Body` -> `Headers` -> `Key` - Authorization и `Value` - Token полученный_токен для отправки любого запроса. 

<br>

## Dreamteam:

[GitHub](https://github.com/Furturnax) | Разработчик - Andrew Fedorchenko 
