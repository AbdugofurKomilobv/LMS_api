from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from courses_app.models import Group

# Faqat admin yoki staff foydalanuvchilar kirishi mumkin bo'lgan permission klass
class AdminUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise PermissionDenied(detail="Sizda bu amalni bajarish huquqi yo'q.")
        return request.user.is_authenticated and request.user.is_admin or request.user.is_staff
    


# ========================================================================================

# Faqat staff, o'qituvchi yoki admin foydalanuvchilarga ruxsat beruvchi permission klass.
# Foydalanuvchi login bo‘lgan va shu 3 roldan biriga ega bo‘lishi kerak.

class AdminOrTeacher(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        group_id = (
            request.data.get("group") 
            if request.method in ["POST", "PUT", "PATCH"]
            else view.kwargs.get("group_id")  # ✅ GET uchun
        )

        if not group_id:
            return False

        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return False

        teacher = getattr(request.user, 'teacher', None)
        if teacher and teacher in group.teacher.all():
            return True

        return False
    

# ===========================================================================================

# Faqat O'quvchi ,admin ,staff ga ruxsat bor
class AdminOrStudent(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise PermissionDenied(detail="Sizda bu amalni bajarish huquqi yo'q.")
        return request.user.is_authenticated and (request.user.is_admin or request.user.is_student or request.user.is_staff)


# ============================================================================================

# Custom permission klass:
# - Faqat obyekt egasi (obj.user == request.user)
# - yoki admin/staff foydalanuvchilar obyektga ruxsat oladi.
# - Foydalanuvchi login bo‘lgan bo‘lishi shart.
class AdminOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            raise PermissionDenied(detail="Sizda bu amalni bajarish huquqi yo'q.")
        return request.user.is_authenticated and (obj.user == request.user or request.user.is_staff or request.user.is_admin)
    

# =======================

class IsAdminOrTeacher(BasePermission):
    def has_permission(self, request, view):
        # Admin uchun ruxsat berish
        if request.user.is_staff:
            return True

        # Teacher bo'lmasa, ruxsat yo'q
        if not hasattr(request.user, 'teacher'):
            return False

        teacher = request.user.teacher

        # group_id ni GET bo‘lsa, kwargs dan, POST/PUT bo‘lsa, data dan olamiz
        group_id = (
            view.kwargs.get('group_id') if request.method == 'GET'
            else request.data.get('group')
        )

        if not group_id:
            return False

        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return False

        # Teacher guruh ichida bormi, tekshiramiz
        return teacher in group.teacher.all()
