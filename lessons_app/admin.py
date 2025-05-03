from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Lesson, Attendance

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'group', 'lesson_date']
    search_fields = ['title', 'group__title']
    list_filter = ['lesson_date']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'lesson', 'is_present', 'timestamp']
    list_filter = ['lesson', 'is_present']
