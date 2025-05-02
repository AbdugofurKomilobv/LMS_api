from django.urls import path, include
from rest_framework.routers import DefaultRouter


from user_app.views import StudentListView, StudentUpdateView, StudentRetrieveAPIView,GetStudenstByIds,StudentGroupsAPIView,CreateStudentAPIView




urlpatterns = [
    path('students/', StudentListView.as_view(), name="all_students"),
    path('update/student/<int:id>/', StudentUpdateView.as_view(), name="update_student"),
    path('student/<int:id>/', StudentRetrieveAPIView.as_view(), name="student"),
    path('get-students-by-ids/',GetStudenstByIds.as_view(),name='students-by-id'),
    path('create/student/',CreateStudentAPIView.as_view(),name='add_student'),
    path('student-groups/<int:student_id>/', StudentGroupsAPIView.as_view(), name="student_groups"),



]