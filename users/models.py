from datetime import date

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError



USER_MIN_AGE = 9


def birth_date_validator(value):
    diff_years = relativedelta(date.today(), value).years()
    if diff_years < USER_MIN_AGE:
        raise ValidationError("User is underage")
    return value


class Location(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=100)
    lat = models.DecimalField(verbose_name='Широта', max_digits=8, decimal_places=6, null=True)
    lng = models.DecimalField(verbose_name='Долгота', max_digits=8, decimal_places=6, null=True)

    class Meta:
        verbose_name = 'Местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class UserRoles:
    USER = 'member'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    choices = (
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
    )


# class User(models.Model):
#     first_name = models.CharField(verbose_name='Имя', max_length=60)
#     last_name = models.CharField(verbose_name='Фамилия', max_length=50)
#     username = models.CharField(verbose_name='Логин', max_length=30, unique=True)
#     password = models.CharField(verbose_name='Пароль', max_length=25)
#     role = models.CharField(verbose_name='Тип', choices=UserRoles.choices, default='member', max_length=13)
#     locations = models.ManyToManyField(Location, verbose_name='Местоположение')
#     age = models.PositiveSmallIntegerField(verbose_name='Возраст', null=True)
#
#     class Meta:
#         verbose_name = 'Пользователь'
#         verbose_name_plural = 'Пользователи'
#
#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"

class User(AbstractUser):
    role = models.CharField(choices=UserRoles.choices, default='member', max_length=13)
    locations = models.ManyToManyField(Location)
    age = models.PositiveSmallIntegerField(null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=150, null=True)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=200)
    birth_date = models.DateField(validators=[birth_date_validator], null=True)
    email = models.EmailField(unique=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


