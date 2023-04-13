Социальная сеть YaTube для публикации постов и картинок
=====

![Python 3.7, 3.8](https://img.shields.io/badge/python-3.9-blue) ![django](https://img.shields.io/badge/Django-3.2-green)

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
6. Запустите коммандой
```
gunicorn --bind 0.0.0.0:80 yatube.wsgi --daemon
Сервис доступен по адресу: http://localhost
```
7. Остановить коммандой
```
pkill -f gunicorn
```

Стек технологий:

![Python](https://img.shields.io/badge/Python-3.9.8-%23254F72?style=flat-square&logo=python&logoColor=yellow&labelColor=254f72)
![Django](https://img.shields.io/badge/Django-2.2.28-0C4B33?style=flat-square&logo=django&logoColor=white&labelColor=0C4B33)
![Django](https://img.shields.io/badge/Django%20REST-3.12.4-802D2D?style=flat-square&logo=django&logoColor=white&labelColor=802D2D)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.1.3-712CF9?style=flat-square&logo=bootstrap&logoColor=white&labelColor=712CF9)
