## Развёртывание проекта локально:
+ Клонировать репозиторий и перейти в него в командной строке:
```shell script
git clone git@github.com:Furturnax/donation.git
```

```shell script
cd donation/
```

+ Cоздать и активировать виртуальное окружение `(Windows/Bash)`:

```shell script
python -m venv venv
```

```shell script
source venv/Scripts/activate
```

+ Установить зависимости из файла `requirements.txt`:
```shell script
python -m pip install --upgrade pip
```

```shell script
pip install -r requirements.txt
```

+ Установить [Docker compose](https://www.docker.com/) на свой компьютер.

+ Создать файл `.env` с переменными окружения в `dev`:

[Примеры переменных окружения](./docker/envfiles/.env.example)

+ Запустить проект через `docker-compose`:
```shell script
docker compose -f docker-compose.dev.yml up --build -d
```

+ Добавить синтетические данные:
```shell script
docker compose -f docker-compose.dev.yml exec django python manage.py load_data
```