Запуск: `cp .env.example .env`, затем `docker compose up --build`.
Создайте пользователя: `docker compose exec web python manage.py createsuperuser`.
Приложение: <http://localhost:8000/>. Остановка: `docker compose down`.

