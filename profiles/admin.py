from django.contrib import admin
from .models import StudentProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'age', 'field_of_study', 'created_at']
    list_filter = ['field_of_study', 'age', 'created_at']
    search_fields = ['user__username', 'user__email', 'field_of_study']
    readonly_fields = ['created_at', 'updated_at']
