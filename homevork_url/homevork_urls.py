from os.path import basename

from rest_framework.routers import DefaultRouter
from django.urls import path, include


from courses_app.views import *
app_name = 'courses'


router = DefaultRouter()

router.register('ustoz uy vazifasi',HomeworkViewSet, basename='homework')
router.register('uy vazifasini-korib chiqish',HomeworkReviewViewSet, basename='homework-reviews')
router.register('student uy vazifasi - topshiriqlari',HomeworkSubmissionViewSet, basename='homework-submissions')

urlpatterns = [
    path('', include(router.urls)),
 
]