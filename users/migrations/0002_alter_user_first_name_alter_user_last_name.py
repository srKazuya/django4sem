# Generated by Django 5.1.6 on 2025-03-06 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(default='Имя', max_length=255, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(default='Фамилия', max_length=255, verbose_name='Имя'),
        ),
    ]
