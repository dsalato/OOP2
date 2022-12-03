from django.contrib import admin

# Register your models here.
from .models import User, Request, Category

admin.site.register(User)
admin.site.register(Category)


@admin.register(Request)
class RequestRegister(admin.ModelAdmin):
    model = Request

    def get_form(self, request, obj=None, **kwargs):
        if obj.status == "new":
            self.exclude = ('photo_done', 'text_commit')
        elif obj.status == "in proqress":
            self.exclude = ('photo_done', 'status')
        else:
            self.exclude = ('status', 'text_commit')

        form = super(RequestRegister, self).get_form(request, obj, **kwargs)
        return form