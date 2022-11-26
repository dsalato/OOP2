from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.crypto import get_random_string


def get_name_file(instance, filename):
    return '/'.join([get_random_string(length=5)+'_'+filename])


def file_size(img):
    limit = 2 * 1024 * 1024
    if img.file.size > limit:
        raise ValidationError('Файл слишком большой. Размер не должен превышать 2 МБ.')


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
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in proqress', 'В процессе'),
        ('completed', 'Завершено')
    ]
    user = models.ForeignKey('User', verbose_name='Пользователь', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=254, verbose_name='Имя', blank=False)
    text = models.TextField(max_length=500, verbose_name='Описание', blank=False)
    text_commit = models.TextField(max_length=500, verbose_name='Комментарий', null=True, blank=True)
    date = models.DateTimeField(verbose_name='Дата_добавления', auto_now_add=True)
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.CASCADE)
    photo_done = models.ImageField(max_length=254, verbose_name='Готовые работы', upload_to=get_name_file, blank=True, null=True,
                                   validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'bmp']),
                                               file_size])
    photo = models.ImageField(max_length=254, verbose_name='Фотография', upload_to=get_name_file, blank=True, null=True,
                              validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'bmp']),
                                          file_size])
    status = models.CharField(max_length=254, verbose_name='Статус',
                              choices=STATUS_CHOICES,
                              default='new')

    def status_verbose(self):
        return dict(self.STATUS_CHOICES)[self.status]

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=254, verbose_name='Название', blank=False)

    def __str__(self):
        return self.name


