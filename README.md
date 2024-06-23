# Проект YaMDb

## Описание проекта 🎑

Проект YaMDb собирает **отзывы** пользователей на **произведения**. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведения делятся на **категории**, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Произведению может быть присвоен **жанр** из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).

## Как запустить проект 🖥️

Клонировать репозиторий с проектом и перейти в соответствующую директорию в командной строке:

```bash
git clone <https://github.com/keisykeij/api_yamdb.git>
cd api_yamdb

```

Создать виртуальное окружение и активировать его:

```bash
python3 -m venv venv
# Mac/Linux
source venv/bin/activate
# Windows
.venv\\Scripts\\activate.bat

```

Установить зависимости для проекта:

```bash
pip install --upgrade pip
pip install -r requirements.txt

```

Выполнить миграции:

```bash
cd api_yamdb
python manage.py migrate

```

Запустить тестовый сервер:

```bash
python manage.py runserver

```

## Примеры запросов 🙈

### Получение списка произведений

[GET] [http://127.0.0.1:8000/api/v1/titles/](http://127.0.0.1:8000/api/v1/posts/)

### Query Params:

| category | string 
фильтрует по полю slug категории |
| --- | --- |
| genre | string 
фильтрует по полю slug жанра |
| name | string 
фильтрует по названию произведения |
| year | integer 
фильтрует по году |

### Responses:

```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "^-$"
        }
      ],
      "category": {
        "name": "string",
        "slug": "^-$"
      }
    }
  ]
}
```

### Добавление произведения

[POST] [http://127.0.0.1:8000/api/v1/titles/](http://127.0.0.1:8000/api/v1/posts/)

### **Authorizations:**

*jwt-token* (`write:admin`)

**Header parameter name:** `Bearer`

**Required scopes:** `write:admin`

### Request Body Scheme: application/json

| name
(required) | string (Название)   <= 256 characters  |
| --- | --- |
| year 
(required) | integer (Год выпуска)  |
| description | string (Описание)  |
| genre 
(required) | Array of strings (Slug жанра)  |
| category 
(required) | string (Slug категории) |

### Responses:

```json
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "^-$"
    }
  ],
  "category": {
    "name": "string",
    "slug": "^-$"
  }
}
```

### **Получение списка всех отзывов**

[GET] http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/

### Path Parametrs

| title_id
(required) | integer 
ID произведения |
| --- | --- |

### Responses

```json
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

### **Добавление нового отзыва**

[POST] [http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/](http://127.0.0.1:8000/api/v1/titles/%7Btitle_id%7D/reviews/)

### **Authorizations:**

*jwt-token* (`write:user,moderator,admin`)

**Header parameter name:** `Bearer`

**Required scopes:** `write:user,moderator,admin`

### Path Parametrs

| title_id
(required) | integer 
ID произведения |
| --- | --- |

### Request Body schema: application/json

| text
(required) | string (Текст отзыва)  |
| --- | --- |
| score
(required) | integer (Оценка)   [ 1 .. 10 ] |

### Response

```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```

### **Получение списка всех комментариев к отзыву**

[GET] [http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/](http://127.0.0.1:8000/api/v1/titles/%7Btitle_id%7D/reviews/%7Breview_id%7D/comments/)

### Path Parameters

| title_id
(required) | integer 
ID произведения |
| --- | --- |
| review_id
(required) | integer 
ID отзыва |

### Response

```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```

### **Добавление комментария к отзыву**

[POST] [http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/](http://127.0.0.1:8000/api/v1/titles/%7Btitle_id%7D/reviews/%7Breview_id%7D/comments/)

### **Authorizations:**

*jwt-token* (`write:user,moderator,admin`)

**Header parameter name:** `Bearer`

**Required scopes:** `write:user,moderator,admin`

### Path Parameters

| title_id
(required) | integer 
ID произведения |
| --- | --- |
| review_id
(required) | integer 
ID отзыва |

### Request Body schema: application/json

| text
(required) | string (Текст комментария) |
| --- | --- |

### Response

```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```

### **Получение комментария к отзыву**

[GET] [http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/](http://127.0.0.1:8000/api/v1/titles/%7Btitle_id%7D/reviews/%7Breview_id%7D/comments/%7Bcomment_id%7D/)

### path Parameters

| title_id
(required) | integer 
ID произведения |
| --- | --- |
| review_id
(required) | integer 
ID отзыва |
| comment_id
(required) | integer 
ID комментария |

### Response

```json
{
"id": 0,
"text": "string",
"author": "string",
"pub_date": "2019-08-24T14:15:22Z"
}
```

### Полное описание доступных действий вы можете найти в документации по адресу: http://127.0.0.1:8000/redoc/

## Команда разработчиков 🧑🏻‍💻

| Должность | ФИ | Контактные данные |  |
| --- | --- | --- | --- |
| TeamLead | Аронов Артем | mailto:keisykeij@yandex.ru |  |
| BackEnd Dev | Герасимов Николай | mailto:Nikolay.Gerasimov495@yandex.ru |  |
| BackEnd Dev | Лебедев Иван | mailto:Ivan_lbd@mail.ru |  |