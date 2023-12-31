# 📋⁉️ Платформа опросов
Тестовое задание:

## Аутентификация и авторизация пользователя:

- Реализуйте регистрацию пользователей и вход в систему с использованием OAuth2.
- Убедитесь, что только прошедшие проверку подлинности пользователи могут создавать, просматривать опросы и взаимодействовать с ними.

## Управление анкетами:

- Разрешить авторизованным пользователям создавать опросы.
- Каждая анкета должна иметь название, описание и список связанных с ней вопросов.
- Внедрите функциональность CRUD для анкет.

## Управление вопросами:

- Пользователи должны иметь возможность добавлять вопросы в свои опросы.
- Вопросы должны иметь текстовое поле и варианты ответов (для вопросов с несколькими вариантами ответов).
- Внедрите функциональность CRUD для вопросов.

## Видимость анкеты:

- Отслеживайте, просматривал ли пользователь опрос или нет.
- Внедрить механизм различия между просмотренными и непросмотренными опросами для каждого пользователя.

## Избранные анкеты:

- Разрешить пользователям ставить лайки/не нравится опросам.
- Отображение количества лайков по каждому опросу.
- Реализовать возможность показывать опросы, отсортированные по количеству лайков.

### Дополнительные задания:

- Добавьте возможность пользователям делиться опросами с другими.
- Внедрить функцию поиска для поиска конкретных опросов.
- Добавляйте уведомления о новых опросах или лайках.
- Создайте панель пользователя для отображения созданных пользователем опросов, понравившихся опросов и просмотренных/непросмотренных опросов.

# Как запустить:
* склонируйте репозиторий ``` git clone https://github.com/Pavel2232/SurveyPlatform  ```
* установите зависимости проекта ```poetry install ```
* заполните .env 
````dotenv
DEBUG=On/Off
SECRET_KEY=your SECRET_KEY
DATABASE_URL=psql://username:password@host:port/db_name
SOCIAL_AUTH_VK_OAUTH2_KEY=your VK_OAUTH2_KEY
SOCIAL_AUTH_VK_OAUTH2_SECRET=your VK_OAUTH2_SECRET
````
* поднимите тестувую базу данных(если есть необходимостьв ней)
```docker
docker-compose up -d
```
````dotenv
DATABASE_URL=psql://test:test@localhost:5432/test
````
* выполните ```./manage.py makemigrations```
* выполните ```./manage.py migrate```
* выполните ```./manage.py runserver```

## Навигация по проекту:
- есть файл для тестирования с уже готовыми данными для бд
````python
./manage.py loaddata db.json
````
- APIDocs [Survey PlatformAPI](Survey%20PlatfotmAPI.yaml)
со данными для взаимодействия.

