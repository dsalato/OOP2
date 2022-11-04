from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.crypto import get_random_string


def get_name_file(instance, filename):
    return '/'.join([get_random_string(length=5)+'_'+filename])


class User(AbstractUser):
    last_name = models.CharField(max_length=254, verbose_name='Фамилия', blank=False)
    first_name = models.CharField(max_length=254, verbose_name='Имя', blank=False)
    patronymic = models.CharField(max_length=254, verbose_name='Отчество', blank=True)
    username = models.CharField(max_length=254, verbose_name='Логин', unique=True, blank=False)
    email = models.CharField(max_length=254, verbose_name='Почта', unique=True, blank=False)
    password = models.CharField(max_length=254, verbose_name='Пароль', blank=False)
    role = models.CharField(max_length=254, verbose_name='Роль',
                            choices=(('admin', 'Администратор'), ('user', 'Пользователь')), default='user')

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.last_name


class Request(models.Model):
    name = models.CharField(max_length=254, verbose_name='Имя', blank=False)
    text = models.TextField(max_length=500, verbose_name='Описание', blank=False)
    date = models.DateTimeField(verbose_name='Дата_добавления', auto_now_add=True)
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.CASCADE)
    photo = models.ImageField(max_length=254, upload_to=get_name_file, blank=True, null=True,
                              validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'bmp'])])
    status = models.CharField(max_length=254, verbose_name='Статус',
                              choices=(('new', 'Новая'), ('in proqress', 'В процессе'), ('completed', 'Завершено')),
                              default='new')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=254, verbose_name='Название', blank=False)

    def __str__(self):
        return self.name