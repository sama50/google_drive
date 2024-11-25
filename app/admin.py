from django.contrib import admin
from .models import File,Folder
# Register your models here.

@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('id','name')


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id','name')
