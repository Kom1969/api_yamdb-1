# API YaMDb
## Групповой проект
### Описание
Проект YaMDb призван помочь отработать навыки групповой разработки с участием трех человек. Проект собирает отзывы пользователей на различные произведения искусства. Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
### Технологии
- Python - язык программирования.
- Django - свободный фреймворк для веб-приложений на языке Python.
- Django REST Framework - мощный и гибкий набор инструментов для создания веб-API.
- Simple JWT - плагин аутентификации JSON Web Token для Django REST Framework.
### Запуск проекта в dev-режиме
- Установите и активируйте виртуальное окружение
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- В папке с файлом manage.py выполните команду:
```
python manage.py runserver
```
### После запуска проекта, документация будет доступна по адресу:
```
http://127.0.0.1:8000/redoc/
```
### Примеры
Регистрация нового пользователя
```
POST http://127.0.0.1:8001/api/v1/auth/signup/
```
```
{
"email": "user@example.com",
"username": "string"
}
```
Получение JWT-токена
```
POST http://127.0.0.1:8001/api/v1/auth/token/
```
```
{
  "username": "string",
  "confirmation_code": "string"
}
```
Получение списка всех категорий
```
GET http://127.0.0.1:8001/api/v1/categories/
```
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
       "slug": "string"
    }
  ]
}
```
Добавление новой категории
```
POST http://127.0.0.1:8001/api/v1/categories/
```
```
{
  "name": "string",
  "slug": "string"
}
```
Удаление категории
```
DELETE http://127.0.0.1:8001/api/v1/categories/{slug}/
```
Получение списка всех жанров
```
GET http://127.0.0.1:8001/api/v1/genres/
```
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
         "name": "string",
      "slug": "string"
    }
  ]
}
```
Добавление жанра
```
POST http://127.0.0.1:8001/api/v1/genres/
```
```
{
  "name": "string",
  "slug": "string"
}
```
Получение информации о произведении
```
GET http://127.0.0.1:8001/api/v1/titles/{titles_id}/
```
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
            "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
Частичное обновление информации о произведении
```
PATH http://127.0.0.1:8001/api/v1/titles/{titles_id}/
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
Получение списка всех отзывов
```
GET http://127.0.0.1:8001/api/v1/titles/{title_id}/reviews/
```
{
     "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```
### Авторы
- Михаил Корюкин
- Роман Иноземцев
- Алена Смирнова
```
https://github.com/Kom1969
```
