Mountain Passes API

REST API для учета горных перевалов с системой модерации.  
Основные функции:
- Добавление новых перевалов с фото
- Редактирование (только для статуса `new`)
- Фильтрация по пользователям
- Модерация (смена статусов)

Технологии
- Python 3.10 + Django 5.0
- Django REST Framework
- PostgreSQL
- Docker
- Swagger/ReDoc

Быстрый старт

1. Клонирование
git clone https://github.com/ваш-репозиторий.git

2. Настройка
cp .env.example .env
nano .env  # Заполните переменные

3. Запуск
docker-compose up --build

Документация API
Основные эндпоинты
POST  `/api/submitData/` - Добавить перевал 
GET  `/api/submitData/?user__email=email` - Фильтр по email 

Пример запроса
json: 
POST /api/submitData/
{
  "user": {
    "email": "test@mail.ru",
    "phone": "+79161234567",
    "fam": "Иванов"
  },
  "title": "Перевал Тестовый"
}

Пример ответа:
json:
{
  "status": 201,
  "id": 123,
  "message": "Успешно создано"
}


Интерфейсы
Доступны после запуска:
- Swagger UI: `http://localhost:8000/swagger/`  
- ReDoc: `http://localhost:8000/redoc/`
