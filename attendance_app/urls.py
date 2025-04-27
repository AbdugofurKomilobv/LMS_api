from django.urls import path, include
from rest_framework.routers import DefaultRouter

from attendance_app.views import StatusViewSet, AttendanceViewSet

app_name = 'attendances'
router = DefaultRouter()
router.register(r'status', StatusViewSet, basename='status')
router.register('attendance', AttendanceViewSet, basename='attendance')

urlpatterns = [
    path('', include(router.urls)),
]