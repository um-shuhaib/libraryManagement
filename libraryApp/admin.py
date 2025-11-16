from django.contrib import admin
from libraryApp.models import User,Category,Book

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Book)
