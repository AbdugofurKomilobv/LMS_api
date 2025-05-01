

from rest_framework.routers import DefaultRouter
from django.urls import path, include


from courses_app.views import *
app_name = 'courses'


router = DefaultRouter()

router.register(r'courses',CourseViewSet, basename='courses')

urlpatterns = [
    path('', include(router.urls)),
    path('group-students/<int:pk>',GroupStudentsAPIView.as_view())
]