set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

# python manage.py shell -c "
# from books.models import Background
# try:
#     obj = Background.objects.get(id=5)
#     obj.url = 'https://mir-s3-cdn-cf.behance.net/project_modules/1400/fcee6692300971.5e47d656aae59.jpg'
#     obj.save()
#     print('Updated URL for entry 5')
# except BooksBackground.DoesNotExist:
#     print('Entry 5 not found')
# "

python manage.py loaddata initial_data.json

if [[ $CREATE_SUPERUSER ]]
then
    python manage.py createsuperuser --no-input
fi
