from django.contrib import admin
from .models import (
    Course, TableType, Table,
    Group, Homework,
    HomeworkSubmission, HomeworkReview,Subject
)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(TableType)
class TableTypeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('room', 'start_time', 'finish_time', 'type')
    search_fields = ('room',)
    list_filter = ('type',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'active')
    search_fields = ('title',)
    filter_horizontal = ('teacher',)
    list_filter = ('active',)


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'group', 'teacher')
    search_fields = ('title',)
    list_filter = ('course', 'group', 'teacher')


@admin.register(HomeworkSubmission)
class HomeworkSubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'homework', 'is_checked')
    list_filter = ('is_checked', 'homework')


@admin.register(HomeworkReview)
class HomeworkReviewAdmin(admin.ModelAdmin):
    list_display = ('submission', 'teacher', 'grade')
    list_filter = ('grade', 'teacher')
    search_fields = ('submission__student__user__full_name',)
