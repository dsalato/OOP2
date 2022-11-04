from django.contrib import admin

# Register your models here.
from .models import User, Request, Category

admin.site.register(User)
admin.site.register(Request)
admin.site.register(Category)