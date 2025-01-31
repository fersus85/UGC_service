# Проектная работа 9 спринта UGC Service 2

1. Развернут ELK и подключен к сервисам.
2. Выполнено исследование по выбору хранилища: MongoDB и Postgres
3. Создано API, реализующее CRUD для работы с закладками, лайками и рецензиями.
4. Развернут и подключен к сервисам Sentry.
5. Написаны конфигурационные файлы для CI в GithubActions.

Ссылка на приватный репозитории с командной работой:
- https://github.com/fersus85/ugc_sprint_2.git

Сопутствующие сервисы из предыдущих спринтов:
- https://github.com/fersus85/Auth_sprint_2.git - сервис Auth + интеграция
- https://github.com/fersus85/Async_API_sprint_2 - сервис Movies_API
- https://github.com/fersus85/Admin_panel - сервис админ панели

## Содержание
- [Описание сервиса](#описание-сервиса)
- [Системные требования](#системные-требования)
- [Настройки](#настройки)
- Запуск
  - [Makefile](#запуск-makefile)
  - [Docker](#запуск-docker)
- [Использование](#использование)
- [Openapi](#openapi)
- [ELK](#ELK)
- [Sentry](#Sentry)
- [Контакты и поддержка](#контакты-и-поддержка)

## Описание сервиса
API сервис, реализующий CRUD для работы с закладками, лайками и рецензиями, с MongoDB в качестве хранилища. Часть онлайн-кинотеатра.
Остальные части:
- **Сервис Аутентификации**: Обеспечивает регистрацию и аутентификацию пользователей, управление учетными записями и безопасность данных. [документация](https://github.com/fersus85/Auth_sprint_2/blob/main/README.md)
- **Сервис Выдачи контента**: Отвечает за предоставление и управление контентом, включая фильмы и сериалы, а также их метаданные. [документация](https://github.com/fersus85/Async_API_sprint_2/blob/main/README.md)
- **Сервис Админ панели**: Предоставляет интерфейс для администраторов, позволяя управлять контентом. [документация](https://github.com/fersus85/Admin_panel/blob/main/README.md)

## Системные требования
- Python 3.10
- Docker
- Docker Compose
- утилита make (опционально)

## Настройки
1. Клонируйте репозиторий:
```bash
  git clone https://github.com/fersus85/ugc_sprint_2.git
```
2. Перейдите в директорию проекта:
```bash
  cd ugc_sprint_2
```
3. Создайте сеть в докере:
```bash
docker network create auth_network
```
4. Настройте .env файлы в сервисах UGC2 и Auth [документация](https://github.com/fersus85/Auth_sprint_2/blob/main/README.md)

## Запуск Makefile
### Auth
1. Запустите сервис Аутентификации:
  [документация](https://github.com/fersus85/Auth_sprint_2/blob/main/README.md)
### UGC2
1. Запустите кластер MongoDB
```bash
make up-mongo
```
2. Проинициализируйте кластер MongoDB
```bash
make init-mongo
```
3. Запустите сервис UGC2
```bash
make up-ugc2
```

## Запуск Docker
### Auth
1. Запустите сервис Аутентификации:
  [документация](https://github.com/fersus85/Auth_sprint_2/blob/main/README.md)
### UGC2
1. Запустите кластер MongoDB
```bash
docker compose -f docker-compose-mongodb.yml up -d --build
```
2. Проинициализируйте кластер MongoDB
```bash
mongo/init.sh
```
3. Запустите сервис UGC2
```bash
docker compose up -d --build
```

## Makefile
все команды makefile можно увидеть, вызвав
```bash
  make help
```

## Использование
После запуска всех сервисов:
- сервис Аутентификации работает на http://127.0.0.1:80 и https://127.0.0.1:443
- сервис UGC2 работает на http://127.0.0.1:82 и https://127.0.0.1:442

## Openapi
- Для тестирования в документации openapi в UGC2 получите токен в сервисе Auth (зарегестрируйтесь и войдите в аккаунт), пройдите по https://localhost:82/api/openapi

## ELK
Для подключения сервиса к ELK:
1. Создайте директорию для данных и дайте доступ для записи
```bash
mkdir deploy/es data
chown -R 1000:1000 ./deploy/esdata
```
2. Запустите контейнер ELK
```bash
make up-elk
```
3. По адресу http://localhost:5601 доступен UI Kibana
4. Чтобы посмотреть логи создайте DataView (Management → Stack Management → Data Views). Введите имя шаблона (UGC-2), и шаблон (ugc-2-logs*). Теперь в Analytics -> Discover можно посмотреть логи.

## Sentry
1. **Установка Sentry:**
   - Выполните команду:
     ```bash
     make install-sentry
     ```
   - Во время установки создайте пользователя, следуя инструкциям.

2. **Запуск Sentry:**
   - Запустите Sentry командой:
     ```bash
     make up-sentry
     ```

3. **Аутентификация:**
   - Откройте браузер и перейдите по адресу [http://localhost:9000](http://localhost:9000).
   - Выполните вход, используя учётные данные, указанные при регистрации.

4. **Создание проекта:**
   - Перейдите в раздел **Projects**.
   - Выберите **Create Project**.
   - Найдите шаблон **FastAPI** и нажмите **Create Project**.

5. **Настройка DSN:**
   - В разделе **Configure SDK** скопируйте строку DSN.
   - Замените в ней `localhost` на `host.docker.internal`.
   - Вставьте полученное значение в файл `.env` в параметр `SENTRY_DSN`.

## Контакты и поддержка
Для получения поддержки или вопросов обращайтесь по электронной почте:
- **Тимлид**: deriabin_85@mail.ru
- **Разработчик**: dmitcvetcov@yandex.ru
- **Разработчик**: maximsonis@gmail.com
