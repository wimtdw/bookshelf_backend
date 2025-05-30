# Generated by Django 3.2.16 on 2025-05-07 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_book_entry_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Название жанра')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'ordering': ['name'],
            },
        ),
        migrations.RemoveField(
            model_name='book',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='book',
            name='isbn',
        ),
        migrations.RemoveField(
            model_name='book',
            name='publication_date',
        ),
        migrations.AddField(
            model_name='book',
            name='cover',
            field=models.URLField(blank=True, null=True, verbose_name='Обложка'),
        ),
        migrations.AddField(
            model_name='book',
            name='publication_year',
            field=models.IntegerField(blank=True, null=True, verbose_name='Год публикации'),
        ),
        migrations.AddField(
            model_name='book',
            name='genres',
            field=models.ManyToManyField(blank=True, to='books.Genre', verbose_name='Жанры'),
        ),
    ]
