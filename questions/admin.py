from django.contrib import admin
from .models import Question

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['order', 'text', 'created_at']
    search_fields = ['text']
    ordering = ['order']

# Désactiver l'admin pour Answer pour éviter les conflits avec Django 4.2.10 + Python 3.14
# admin.site.register(Answer, AnswerAdmin)
