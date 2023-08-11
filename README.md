# DenisKtv-test-referal- это API реализовывающее простую реферальную систему

![example workflow](https://github.com/DenisKtv/DenisKtv-test-referral/actions/workflows/main.yml/badge.svg)  

## Стек технологий

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![HTML](https://img.shields.io/badge/-HTML-E34F26?style=flat-square&logo=HTML5&logoColor=white)](https://www.w3.org/TR/html52/)
[![CSS](https://img.shields.io/badge/-CSS-1572B6?style=flat-square&logo=CSS3&logoColor=white)](https://www.w3.org/Style/CSS/Overview.en.html)
[![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?style=flat-square&logo=JavaScript&logoColor=black)](https://www.ecma-international.org/publications/standards/Ecma-262.htm)

## Описание проекта

Проект позволяет пользователям легко авторизоваться и зарегистрироваться по номеру телефона. Во время регистрации генерируется верификационный код, эмулируя отправку SMS. Этот код хранится в памяти 90 секунд. После успешной регистрации каждый пользователь получает уникальный инвайт-код. Пользователи могут один раз использовать чужой инвайт-код и также просматривать свой собственный. По номеру телефона можно запросить список телефонных номеров, которые воспользовальс инвайт-кодом данного пользователя.


## Установка проекта локально

* Склонировать репозиторий на локальную машину:
```bash
git clone https://github.com/DenisKtv/DenisKtv-test-referral.git
cd DenisKtv-test-referral/
```

* Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
. venv/bin/activate
```

* Cоздайте файл `.env` в директории `/infra/` с содержанием:

```
Django:
SECRET_KEY = 

telegram chat:
MY_CHAT = 
GROUP_ID =

Postgresql:
DB_ENGINE = 
DB_NAME = 
POSTGRES_USER = 
POSTGRES_PASSWORD = 
HOST = 
PORT = 
```

* Установить зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

* Выполните миграции:

```bash
python manage.py migrate
```

* Запустите сервер:
```bash
python manage.py runserver
```

## Запуск проекта в Docker контейнере
* Установите Docker.

Параметры запуска описаны в файлах `docker-compose.yml` и `nginx.conf` которые находятся в директории `infra/`.  
При необходимости добавьте/измените адреса проекта в файле `nginx.conf`

* Запустите docker-compose:
```bash
docker-compose up -d --build
```  
  > После сборки появляются 3 контейнера:
  > 1. контейнер базы данных **db**
  > 2. контейнер приложения **web**
  > 3. контейнер web-сервера **nginx**
* Примените миграции:
```bash
docker-compose exec backend python manage.py migrate
```
* Создайте администратора:
```bash
docker-compose exec backend python manage.py createsuperuser
```
* Соберите статику:
```bash
docker-compose exec backend python manage.py collectstatic --no-input
```

## Страница для теста:
Страница доступна по ссылке:
[http://185.107.237.87:81/signup/](http://185.107.237.87:81/signup/)

## Документация к API:
API документация доступна по ссылке (создана с помощью redoc):
[http://185.107.237.87:81/redoc/](http://185.107.237.87:81/redoc/)

## Скрины шаблонов:
<img src="1.png" alt="Alt text" title="Optional Title" width="400" />
<img src="2.png" alt="Alt text" title="Optional Title" width="400" />
<img src="3.png" alt="Alt text" title="Optional Title" width="400" />
<img src="4.png" alt="Alt text" title="Optional Title" width="400" />
<img src="5.png" alt="Alt text" title="Optional Title" width="400" />