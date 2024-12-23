from django.contrib import admin
from .models import Category,Products
# Register your models here.


class categoryAdmin(admin.ModelAdmin):
    list_display=('name','image','description')

admin.site.register(Category,categoryAdmin)
admin.site.register(Products)


