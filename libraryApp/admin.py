from django.contrib import admin
from libraryApp.models import User,Category,Book,Issue

# Register your models here.
admin.site.register(User)
admin.site.register(Category)

class BookModel(admin.ModelAdmin):
    exclude=["user"]

    def save_model(self, request, obj, form, change):
        if not change:    #new add cheyyumbol ---- update cheyyumbol owner maran NOT ozhivakkiya madhi
            obj.user=request.user
        return super().save_model(request, obj, form, change)
admin.site.register(Book,BookModel)
admin.site.register(Issue)


