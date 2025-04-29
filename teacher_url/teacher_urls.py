from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user_app.views import TeacherListView,TeacherUpdateView,TeacherRetrieveAPIView,GetTeacherByIds,TeacherCreateView,TeacherGrouView,TeacherGroupDetailAPIView

app_name = 'users'

router = DefaultRouter()
# router.register(r'parents', ParentViewSet, basename='parent')

urlpatterns = [
    path('teachers/', TeacherListView.as_view(), name="all_teachers"),
    path('update/teacher/<int:id>/', TeacherUpdateView.as_view(), name="update_teacher"),
    path('teacher/<int:id>/', TeacherRetrieveAPIView.as_view(), name="teacher"),
    path('get-teachers-by-ids/',GetTeacherByIds.as_view(),name='teachers-by-id'),
    path('create-teacher/',TeacherCreateView.as_view(),name='ctreate-teacher'),
    path('teacher-group/<int:teacher_id>/',TeacherGrouView.as_view()),
    path('teacher/teacher-group/<int:teacher_id>/<int:group_id>/', TeacherGroupDetailAPIView.as_view()),




]