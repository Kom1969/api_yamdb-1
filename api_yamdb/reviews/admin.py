from django.contrib import admin

# Register your models here.
from .models import Category, Genre, Title

admin.site.register(Category, admin.ModelAdmin)
admin.site.register(Genre, admin.ModelAdmin)
admin.site.register(Title, admin.ModelAdmin)
