from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('accounts/profile/', Profile.as_view(), name='profile'),
    path('requests/', CreateRequests.as_view(), name='requests'),
    path(r'^request/(?P<pk>\d+)/delete/$', RequestDelete.as_view(), name='request_delete'),
    path(r'^request/(?P<pk>\w+)/(?P<st>\w+)/update/$', request_update, name='request_update'),
    path('category_list', category_list, name='category_list'),
    path('create_category/', CreateCategory.as_view(), name='create_category'),
    path(r'^category/(?P<pk>\d+)/delete/$', CategoryDelete.as_view(), name='category_delete')
]