# Generated by Django 4.1.1 on 2022-10-09 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('member', 'Пользователь'), ('admin', 'Администратор'), ('moderator', 'Модератор')], default='member', max_length=13, verbose_name='Тип'),
        ),
    ]
