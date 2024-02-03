# Django REST API Picasso

### Проект, который позволяет загружать файлы на сервер, а затем асинхронно обрабатывать их с использованием Celery.

# Описание проекта
Проект состоит из 3 контейнеров: backend, nginx и redis. Celery запускается внутри контейнера бэкенда. База данных хранится в volume в `sqlite_db`. Файлы, отправленные по API сохраняются в volume `files`. Статика хранитя в volume `static`. Celery изменяет поле processed после отправки запроса на эндпоинт `/upload`. Эндпоинт `/files` возвращает список файлов, хранимых в базе данных. 

Покрытие тестами 91%. Измерял с помощью `coverage`.

Тестирование API производил с помощью Postman.



# Установка, настройка и запуск проекта

1. Копируем репозиторий с помощью `git clone git@github.com:daniil-orlovv/picasso_celery_files.git`
2. Устанавливаем и активируем виртуальное окружение: `python -m venv venv` → `source venv/scripts/activate`
3. с помощью терминала переходим в директорию, где расположен `docker-compose.yml`
4. Запускаем докер компоуз: `docker compose up`
5. Заходим в контейнер `picasso-backend-1` с помощью `winpty docker exec -it picasso-backend-1 bash`
6. Создаем и запускаем миграции внутри контейнера, перейдя в директорию, где расположен `manage.py`: `python manage.py makemigrations` → `python manage.py migrate`
7. Собираем и копируем статику: `python manage.py collectstatic` → `cp -r /app/collected_static/. /backend_static/static/`
8. Создаем суперюзера, если необходимо зайти в админку: `python manage.py createsuperuser`
9. Запускаем Celery: `celery -A picasso worker -l info --pool=solo`

Теперь проект запущен и работает. Celery ожидает задачи. Бэкенд обрабатывает запросы через API.


# Изменение архитектуры при увеличении нагрузки

**База данных:**
SQLite может столкнуться с проблемами масштабирования при высокой нагрузке. Необходим переход к более масштабируемой базе данных, такой как PostgreSQL или MySQL, особенно если часто происходят операции записи или обновления.

**Кэширование:**
Введение кэширования может существенно снизить нагрузку на базу данных. Необходимо использование инструмента кэширования, такого как Redis, для хранения результатов часто запрашиваемых запросов.

**Балансировка нагрузки:**
Внедрение балансировщика нагрузки для распределения запросов между несколькими серверами. Это поможет улучшить производительность и обеспечить отказоустойчивость.

**Микросервисная архитектура:**
Необходимо разбить функционал API на микросервисы. Это позволит масштабировать только те компоненты, которые действительно подвергаются высокой нагрузке, не затрагивая другие части системы.
