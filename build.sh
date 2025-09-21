set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

python manage.py shell -c "
from books.models import Background
try:
    obj = Background.objects.get(id=3)
    obj.url = 'https://i.pinimg.com/originals/75/f7/a3/75f7a3732d6953e9ab5d437ff851721b.jpg'
    obj.save()
    print('Updated URL for entry 3')
except BooksBackground.DoesNotExist:
    print('Entry 3 not found')
"

# python manage.py loaddata initial_data.json

# if [[ $CREATE_SUPERUSER ]]
# then
#     python manage.py createsuperuser --no-input
# fi
