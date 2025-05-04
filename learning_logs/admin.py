from django.contrib import admin
from .models import Topic, Entry

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('text', 'date_added', 'private')

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('topic', 'text', 'date_added', 'private')
