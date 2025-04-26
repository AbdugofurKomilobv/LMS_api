from os.path import basename

from rest_framework.routers import DefaultRouter
from django.urls import path, include

from courses_app.views import GroupViewSet,GetGroupByIds,SubjectViewSet,CourseViewSet,TableViewSet,HomeworkViewSet,HomeworkReviewViewSet,HomeworkSubmissionViewSet

app_name = 'courses'


router = DefaultRouter()
router.register(r'groups',GroupViewSet, basename='group')
router.register(r'subjects',SubjectViewSet, basename='subject')
router.register(r'courses',CourseViewSet, basename='courses')
router.register(r'table',TableViewSet, basename='table')

# Uy vazifasi bo'limlari
router.register('ustoz uy vazifasi',HomeworkViewSet, basename='homework')
router.register('uy vazifasini-korib chiqish',HomeworkReviewViewSet, basename='homework-reviews')
router.register('student uy vazifasi - topshiriqlari',HomeworkSubmissionViewSet, basename='homework-submissions')

urlpatterns = [
    path('', include(router.urls)),
    # path('get-groups-by-ids/',GetGroupByIds.as_view(), name='get-groups-by-ids/')
]