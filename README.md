# Markets-Bridge
## Установка
### Конфигурация системы
Для функционирования системы необходимы: 
- PostgreSQL база (https://www.postgresql.org/);
- RabbitMQ server (https://www.rabbitmq.com/download.html);
- Поддерживаемая версия Python (>=3.9).
### Установка проекта
Клонируем проект в необходимую директорию:
```shell
git clone git@github.com:qckzzi/markets-bridge-drf-app.git
```
```shell
cd markets-bridge-drf-app
```
Создадим виртуальное окружение:
```shell
python3 -m venv venv
```
(или любым другим удобным способом)

Активируем его:
```shell
. venv/bin/activate
```
Установим зависимости:

(для разработки)
```shell
pip install -r DEV_REQUIREMENTS.txt
```
(для деплоя)
```shell
pip install -r REQUIREMENTS.txt
```
В корневой директории проекта необходимо скопировать файл ".env.example", переименовать
его в ".env" и заполнить в соответствии с вашей системой.
В том числе необходимо сгенерировать свой SECRET_KEY для django ([Создание SECRET_KEY](https://www.educative.io/answers/how-to-generate-a-django-secretkey)).

Запуск проекта:
```shell
python markets_bridge/manage.py runserver
```
## Разработка

Для внесения изменений в кодовую базу необходимо инициализировать pre-commit git hook.
Это можно сделать командой в терминале, находясь в директории проекта:
```shell
pre-commit install
```