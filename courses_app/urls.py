from os.path import basename

from rest_framework.routers import DefaultRouter
from django.urls import path, include

from courses_app.views import GroupViewSet

app_name = 'courses'


router = DefaultRouter()
router.register(r'groups',GroupViewSet, basename='group')

urlpatterns = [
    path('', include(router.urls)),
]