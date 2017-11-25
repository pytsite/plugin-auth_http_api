# PytSite Authentication HTTP API version 1


## POST auth/access-token/:driver

Создание токена доступа.


### Аргументы

- `driver`: имя драйвера аутентификации.


### Параметры

- *required* аргументы драйвера аутентификации.


### Формат ответа

Объект.

- **str** `token`. Токен доступа.
- **str** `user_uid`. Идентификатор учётной записи владельца токена доступа.
- **int** `ttl`. Срок действия токена доступа в секундах.
- **str** `created`. Время создания токена доступа в формате W3C.
- **str** `expires`. Время истечения токена доступа в формате W3C.


### Примеры

Получение токена доступа через драйвер 'password'. Параметры `login` и `password` являются аргументами драйвера:

```
curl -X POST \
-d login=vasya@pupkeen.com \
-d password=Very5tr0ngP@ssw0rd \
https://test.com/api/1/auth/access-token/password
```


Ответ:

```
{
    "token": "e51081bc4632d8c2a31ac5bd8080af1b",
    "user_uid": "586aa6a0523af53799474d0d",
    "ttl": 86400,
    "created": "2017-01-25T14:04:35+0200",
    "expires": "2017-01-26T14:04:35+0200"
}
```


## GET auth/access-token/:token

Получение информации о токене доступа.


### Аргументы

- `token`. Токен доступа.


### Фомат ответа

Объект.

- **str** `token`. Токен доступа.
- **str** `user_uid`. Идентификатор учётной записи владельца токена доступа.
- **int** `ttl`. Срок действия токена доступа в секундах.
- **str** `created`. Время создания токена доступа в формате W3C.
- **str** `expires`. Время истечения токена доступа в формате W3C.


### Примеры

Запрос:

```
curl -X GET https://test.com/api/1/auth/access-token/e51081bc4632d8c2a31ac5bd8080af1b
```

Ответ:

```
{
    "token": "e51081bc4632d8c2a31ac5bd8080af1b",
    "user_uid": "586aa6a0523af53799474d0d",
    "ttl": 86400,
    "created": "2017-01-25T14:04:35+0200",
    "expires": "2017-01-26T14:04:35+0200"
}
```


## DELETE auth/access-token/:token

Удаление ранее созданного токена доступа.


### Аргументы

- `token`. Токен доступа.


### Формат ответа

В случае отсутствия ошибок метод всегда возвращает объект вида `{status: true}`.


### Примеры

Запрос:

```
curl -X DELETE https://test.com/api/1/auth/access-token/e51081bc4632d8c2a31ac5bd8080af1b
```


Ответ:

```
{
  "status": true
}
```



## GET auth/user/:uid

Получение информации об учётной записи пользователя.


### Аргументы

- `uid`. Идентификатор учётной записи.


### Формат ответа

Объект.

Поля, возвращаемые всегда:

- **str** `uid`. Идентификатор учётной записи.

Поля, возвращаемые в случае, если `profile_is_public` возвращаемой учётной записи равен `true`, запрашивающая учётная 
запись является администратором или владельцем запрашиваемой учётной записи:

- **str** `profile_url`. URL профиля учётной записи.
- **str** `nickname`. Никнейм.
- **object** `picture`. Юзерпик.
    - **str** `url`. URL.
    - **int** `width`. Ширина в пикселях.
    - **int** `height`. Высота в пикселях.
    - **int** `length`. Размер в байтах.
    - **str** `mime`. MIME-тип.
- **str** `first_name`. Имя.
- **str** `last_name`. Фамилия.
- **str** `full_name`. Имя и фамилия.
- **str** `birth_date`. Дата рождения в формате W3C.
- **str** `gender`. Пол: 'm' -- мальчик, 'f' -- девочка.
- **str** `phone`. Номер телефона.
- **array\[str\]** `follows`. UID учётных записей, на которые подписан пользователь.
- **int** `follows_count`. Количество учётных записей, на которые подписан пользователь.
- **array\[str\]** `followers`. UID учётных записей, которые подписаны на пользователя.
- **int** `followers_count`. Количество учётных записей, которые подписаны на пользователя.
- **bool** `is_followed`. Является ли учётная запись, выполняющая запрос, подписчиком пользователя.
- **bool** `is_follows`. Является ли пользователь подписчиком учётной записи, выполняющей запрос.
- **array\[str\]** `urls`. URL профилей пользователя в других местах.

Дополнительные поля, возвращаемые в случае, если запрашивающая учётная запись является администратором или владельцем 
запрашиваемой учётной записи.

- **str** `created`. Время созания учётной записи в формате W3C.
- **str** `login`. Логин.
- **str** `email`. Email.
- **str** `last_sign_in`. Время последней успешной аутентификации в формате W3C. 
- **str** `last_activity`. Время последней активности в формате W3C.
- **int** `sign_in_count`. Общее количество успешных аутентификаций.
- **str** `status`. Статус учётной записи: 'active', 'waiting' или 'disabled'.
- **bool** `profile_is_public`. Видимость профиля для всех.
- **array\[str\]** `roles`. UID назначенных ролей.
- **array\[str\]** `blocked_users`. UID заблокированных пользователей.

Также возможно добавление дополнительных полей сторонними модулями.


### Примеры

Запрос:

```
curl -X GET \
-H 'PytSite-Auth: e51081bc4632d8c2a31ac5bd8080af1b' \  
https://test.com/api/1/auth/user/576563ef523af52badc5beac
```


Ответ:

```
{
  "uid": "576563ef523af52badc5beac",
  "profile_url": "https://test.com/auth/profile/pupkeen",
  "nickname": "pupkeen",
  "picture": {
    "url": "https://test.com/image/resize/0/0/59/e0/0b544b26210ca43f.png",
    "width": 250,
    "height": 250,
    "length": 41233,
    "mime": "image/png"
  },
  "first_name": "Vasily",
  "last_name": "Pupkeen",
  "full_name": "Vasily Pupkeen",
  "birth_date": "1984-07-05T11:19:18+0300",
  "gender": "m",
  "phone": "+380501234567",
  "follows": [],
  "follows_count": 0,
  "followers":
  [
      "576562d9523af52985715b6b"
  ],
  "followers_count": 1,
  "urls":
  [
      "https://plus.google.com/+Vasyok"
  ],
  "created": "2010-03-17T11:19:18+0300",
  "login": "vasya@pupkeen.com",
  "email": "vasya.p@gmail.com",
  "last_sign_in": "2016-09-12T01:22:56+0300",
  "last_activity": "2016-09-12T11:19:18+0300",
  "sign_in_count": 14,
  "status": "active",
  "profile_is_public": true,
  "roles":
  [
      "57d665063e7d8960ed762231"
  ],
  "blocked_users":
  [
      "57d665063e7d8960e33af78e"
  ]
}
```


## GET auth/users

Получение информации об учётных записях пользователей.


### Параметры

- *required* **array\[str\]** `uids`. Идентификаторы учёных записей.


### Формат ответа

Массив объектов. Формат каждого объекта идентичен возвращаемому
**GET auth/user/:uid**.


### Примеры

Запрос:

```
curl -X GET \
-d uids='["590ed572523af516d789a063", "590ed5f3523af516d789a0cd"]' \
https://test.com/api/1/auth/users
```


Ответ:

```
[
  {
    "uid": "590ed572523af516d789a063",
    ...
  },
  {
    "uid": "590ed5f3523af516d789a0cd",
    ...
  }
]
```


## PATCH auth/user/:uid

Изменение учётной записи пользователя. Обязательна авторизация

### Аргументы

- `uid`. Идентификатор учётной записи.


### Параметры

- **str** `email`. Адрес электронной почты.
- **str** `nickname`. Никнейм.
- **str** `picture`. UID изображения.
- **str** `first_name`. Имя.
- **str** `last_name`. Фаимлия.
- **str** `description`. Описание.
- **str** `birth_date`. Дата рождения в формате W3C.
- **str** `gender`. Пол: `m` -- мальчик, `f` -- девочка.
- **str** `phone`. Номер телефона.
- **str** `country`. Страна.
- **str** `city`. Город.
- **array\[str\]** `urls`. URL профилей пользователя в других местах.
- **bool** `profile_is_public`. Видимость профиля для всех.


### Формат ответа

Смотри **GET auth/user/:uid**.


### Примеры

Запрос:

```
curl -X PATCH \
-H 'PytSite-Auth: e51081bc4632d8c2a31ac5bd8080af1b' \
-d email=hello@world.com \
-d first_name=Hello \
-d last_name=World \
-d gender=f \
-d profile_is_public=false \
-d description='I am an invisible girl' \
https://test.com/api/1/auth/user/576563ef523af52badc5beac
```


## POST auth/follow/:uid

Фолловинг пользователя. Обязательна авторизация.


### Аргументы

- `uid`. Идентификатор учётной записи для фолловинга.


### Формат ответа

Объект.

- **array\[str\]** `follows`. Список UID учётных записей, фолловером которых является учётная запись, выполнявшая запрос.


### Примеры

Запрос:

```
curl -X POST \
-H 'PytSite-Auth: e51081bc4632d8c2a31ac5bd8080af1b' \
https://test.com/api/1/auth/follow/576563ef523af52badc5beac
```

Ответ:

```
{
    "follows": ["576563ef523af52badc5beac"]
}
```


## DELETE auth/follow/:uid

Анфолловинг пользователя. Обязательна авторизация. 


### Аргументы

- `uid`. Идентификатор учётной записи для анфолловинга.


### Формат ответа

Объект.

- **array\[str\]** `follows`. Список UID учётных записей, фолловером которых является учётная запись, выполнявшая запрос.


### Примеры

Запрос:

```
curl -X DELETE \ 
-H 'PytSite-Auth: e51081bc4632d8c2a31ac5bd8080af1b' \
https://test.com/api/1/auth/follow/576563ef523af52badc5beac
```

Ответ:

```
{
    "follows": []
}
```


## POST auth/block_user/:uid

Блокировка пользователя. Обязательна авторизация.


### Аргументы

- `uid`. Идентификатор блокируемой учётной записи.


### Формат ответа

- **array\[str\]** `blocked_users`. UID заблокированных учётных записей.


### Примеры

Запрос:

```
curl -X POST \
-H 'PytSite-Auth: e51081bc4632d8c2a31ac5bd8080af1b' \
https://test.com/api/1/auth/block_user/576563ef523af52badc5beac
```

Ответ:

```
{
    "blocked_users": ["576563ef523af52badc5beac"]
}
```


## DELETE auth/block_user/:uid

Отмена блокировки пользователя. Обязательна авторизация.


### Аргументы

- `uid`. Идентификатор заблокированной учётной записи.


### Формат ответа

- **array\[str\]** `blocked_users`. UID заблокированных учётных записей.


### Примеры

Запрос:

```
curl -X DELETE \
-H 'PytSite-Auth: e51081bc4632d8c2a31ac5bd8080af1b' \
https://test.com/api/1/auth/block_user/576563ef523af52badc5beac
```

Ответ:

```
{
    "blocked_users": []
}
```
