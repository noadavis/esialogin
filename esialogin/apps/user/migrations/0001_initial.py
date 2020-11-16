# Generated by Django 3.1.3 on 2020-11-14 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('datecreated', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('datechanged', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('snils', models.CharField(default='', max_length=20, verbose_name='SNILS')),
                ('fullname', models.CharField(default='user', max_length=200, verbose_name='ФИО')),
                ('email', models.CharField(default='', max_length=40, verbose_name='Эл. почта')),
                ('phone', models.CharField(default='', max_length=20, verbose_name='Телефон')),
            ],
            options={
                'verbose_name': 'Информация о пользователе',
                'verbose_name_plural': 'Информация о пользователях',
            },
        ),
        migrations.CreateModel(
            name='UserLogin',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('datecreated', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('datechanged', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('login', models.CharField(max_length=20, verbose_name='LOGIN')),
                ('snils', models.CharField(default='0', max_length=20, verbose_name='SNILS')),
                ('password_hash', models.CharField(max_length=40, verbose_name='Хэш пароля')),
                ('session_hash', models.CharField(max_length=40, verbose_name='Хэш сессии')),
                ('enabled', models.BooleanField(default=True, verbose_name='Активен?')),
            ],
            options={
                'verbose_name': 'Логин пользователя',
                'verbose_name_plural': 'Логин пользователей',
            },
        ),
    ]
