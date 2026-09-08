# Mini-Social API

Небольшой backend для мини-социальной сети на Django REST Framework.

Есть пользователи, посты, лайки и комментарии. Для авторизации используется JWT, фоновые задачи выполняются через Celery.

## Стек

* Django REST Framework
* SimpleJWT
* PostgreSQL
* Redis
* Celery / Celery Beat
* Docker / Docker Compose

## Запуск

Клонируем репозиторий:

```bash
git clone https://github.com/Askarbek21/medicalka-test.git
cd medicalka-test
```

Запускаем проект:

```bash
docker compose up --build
```

После запуска будет доступна документация:

http://localhost:8000/api/docs/

## Админка

При запуске автоматически создаётся суперпользователь:

```text
username: admin
password: admin123
```

## Тесты

```bash
docker compose exec app python manage.py test
```
