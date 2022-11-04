from django.urls import path
from django.contrib.auth import views as auth_views

from .views import index, RegisterView, LogoutView

urlpatterns = [
    path('', index, name='index'),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
]