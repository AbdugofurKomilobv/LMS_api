from django.contrib import admin

# Register your models here.

from .models import Homework, HomeworkAnswer

class HomeworkAnswerInline(admin.TabularInline):
    model = HomeworkAnswer
    extra = 1

class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'group', 'deadline')
    search_fields = ('title', 'lesson__title', 'group__title')
    list_filter = ('lesson', 'group', 'deadline')
    inlines = [HomeworkAnswerInline]

class HomeworkAnswerAdmin(admin.ModelAdmin):
    list_display = ('student', 'homework', 'submitted_at', 'is_graded', 'grade')
    list_filter = ('is_graded', 'submitted_at', 'homework')
    search_fields = ('student__user__phone', 'homework__title')

admin.site.register(Homework, HomeworkAdmin)
admin.site.register(HomeworkAnswer, HomeworkAnswerAdmin)
