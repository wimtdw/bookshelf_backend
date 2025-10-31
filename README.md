## Бэкенд для приложения "Виртуальная книжная полка"
Технологии: Python, Django, Django REST Framework, PostgreSQL.

Предоставляет API для управления книгами, полками и достижениями. 
API доступен всем для чтения, и только аутентифицированным пользователям для создания объектов и внесения изменений. 
В проекте использована аутентификация по токену JWT.

### Как запустить проект:

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
