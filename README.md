## Бэкенд для приложения "Виртуальная книжная полка"
Технологии: Python, Django, Django REST Framework, PostgreSQL.

Предоставляет API для управления книгами, полками и достижениями. 
API доступен всем для чтения, и только аутентифицированным пользователям для создания объектов и внесения изменений. 
В проекте использована аутентификация по токену JWT.

### Приложение задеплоено на Render и доступно по ссылке https://bookshelf-frontend-2cvm.onrender.com

### !!! После открытия ссылки нужно подождать около минуты, чтобы всё заработало (особенность бесплатного плана Render, приложение замедляется в периоды неактивности) !!!

### Как запустить проект локально:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/wimtdw/bookshelf_backend.git
```

```
cd bookshelf_backend
```

Cоздать и активировать виртуальное окружение:

* Windows
```
python -m venv venv

source venv/Scripts/activate
```
* Linux 
```
python3 -m venv venv

source venv/bin/activate 
`````` 

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```
