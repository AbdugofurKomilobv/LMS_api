from django.contrib import admin
from .models import (
    Course, TableType, Table,
    Group
)




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
    

