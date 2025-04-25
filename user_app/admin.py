from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Student, Teacher, Parent


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('phone', 'full_name', 'is_admin', 'is_teacher', 'is_student', 'is_active')
    list_filter = ('is_admin', 'is_teacher', 'is_student', 'is_active')
    search_fields = ('phone', 'full_name')
    ordering = ('-created',)
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin', 'is_student', 'is_teacher', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2'),
        }),
    )
    filter_horizontal = ('groups', 'user_permissions')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__phone',)
    filter_horizontal = ('group', 'course')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__phone',)
    filter_horizontal = ('course',)


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'phone')
    search_fields = ('name', 'surname', 'phone')
    filter_horizontal = ('students',)
