# Generated by Django 3.2.16 on 2025-05-07 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_auto_20250507_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='order',
            field=models.IntegerField(default=100, unique=True, verbose_name='Порядок'),
        ),
    ]
