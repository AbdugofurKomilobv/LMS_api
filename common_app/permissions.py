from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


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
        if not request.user.is_authenticated:
            raise PermissionDenied(detail="Sizda bu amalni bajarish huquqi yo'q.")
        return request.user.is_authenticated and (request.user.is_staff or request.user.is_teacher or request.user.is_admin)
    

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