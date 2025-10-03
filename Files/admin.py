from django.contrib import admin
from unfold.admin import ModelAdmin
from dal import autocomplete
from django import forms
from .models import *

class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    list_filter = ('name',)

class FileAdmin(ModelAdmin):
    list_display = ('name', 'category', 'created_at')
    search_fields = ('name', 'category__name', )
    list_filter = ('category', )
    readonly_fields = ('created_at','code','image')
    autocomplete_fields = ['category',]


admin.site.register(File,FileAdmin)
admin.site.register(Category,CategoryAdmin)
