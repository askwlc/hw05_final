Социальная сеть YaTube для публикации постов и картинок
=====

[![Python](https://img.shields.io/badge/-Python-464641?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-464646?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![Unittest](https://img.shields.io/badge/Unittest-464646?style=flat-square&logo=pytest)](https://docs.pytest.org/en/6.2.x/)
[![SQLite3](https://img.shields.io/badge/-SQLite3-464646?style=flat-square&logo=SQLite)](https://www.sqlite.org/)

## Описание:

Сервис для публикации личных дневников. Пользователь может зарегистрироваться и создать свою страницу, зайдя на которую можно посмотреть все записи автора. Зарегистрированные пользователи имеют возможность подписываться на авторов и оставлять комментарии к их записям. Незарегистрированные пользователи могут только просматривать записи авторов и комментарии к ним.

### Возможности проекта:
- Регистрация с расширенным профилем и управление им (переопределение модели User с помощью AbstractUser).
- Публикация записей с изображениями.
- Публикация записей в сообщества.
- Комментарии к записям других авторов.
- Подписка на других авторов.
- Лента с записями, на которых оформлена подписка.
- Template tags, отображающие самые обсуждаемые записи, последние записи и пр.
- Для проекта написаны тесты Unittest.


## Установка и запуск на примере Linux:

1. Клонируйте репозиторий с помощью git
```
git clone https://github.com/askwlc/hw05_final.git
```
2. Создайте виртуальное окружение активируйте и установите зависимости
```
cd ./hw05_final
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Создайте файл .env с переменными окружения в корне приложения и добавьте в него следующий параметр:
```
SECRET_KEY=')=(vp1)y(m0h2e86c01lm+$-72i#na)*i4e3$3@663re&_wx%4' # секретный ключ Django (установите свой)
```
4. Выплните миграцию и соберите статику
```
python manage.py migrate
python manage.py collectstatic
```
5. Создайте суперпользователя Django
```
python manage.py createsuperuser
```
6. Запустите проект
```
python manage.py runserver
```
