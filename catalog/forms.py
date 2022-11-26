from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import User, Request, Category
from django import forms


class RegisterUserForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя',
                                 validators=[RegexValidator('^[а-яА-Я- ]+$',
                                                            message='Разрешены только кириллица и дефис')],
                                 error_messages={
                                       'required': 'Обязательное поле',
                                 })
    last_name = forms.CharField(label='Фамилия',
                                validators=[RegexValidator('^[а-яА-Я- ]+$',
                                                           message='Разрешены только кириллица и дефис')],
                                error_messages={
                                   'required': 'Обязательное поле',
                                })
    patronymic = forms.CharField(label='Отчество',
                                 required=False,
                                 validators=[RegexValidator('^[а-яА-Я- ]+$',
                                                            message='Разрешены только кириллица и дефис')])
    email = forms.EmailField(label='Электронная почта',
                             error_messages={
                                 'invalid': 'Не правильный формат адреса',
                                 'unique': 'Данный адрес занят'
                             })
    username = forms.CharField(label='Логин',
                               validators=[RegexValidator('^[a-zA-Z-]+$',
                                                          message='Разрешены только латиница и дефис')],
                               error_messages={
                                   'required': 'Обязательное поле',
                                   'unique': 'Данный логин занят'
                               })
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput,
                               error_messages={
                                     'required': 'Обязательное поле',
                               })
    password2 = forms.CharField(label='Пароль повторно',
                                widget=forms.PasswordInput,
                                error_messages={
                                     'required': 'Обязательное поле',
                                })
    rules = forms.BooleanField(required=True,
                               label='Согласие на обработку данных',
                               error_messages={
                                   'required': 'Обязательное поле',
                               })

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError({
                'password2': ValidationError('Введенные пароли не совпадают', code='password_error')
            })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'patronymic', 'email',
                  'username', 'password', 'password2', 'rules')


class CreateRequestForm(forms.ModelForm):

    class Meta:
        model = Request
        fields = ['name', 'text', 'category', 'photo']


class CreateCategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name']


class DonePhotoRequests(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['photo_done']


class CommitRequests(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['text_commit']