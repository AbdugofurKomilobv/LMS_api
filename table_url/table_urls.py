from os.path import basename

from rest_framework.routers import DefaultRouter
from django.urls import path, include


from courses_app.views import *
app_name = 'courses'


router = DefaultRouter()


router.register(r'table',TableViewSet, basename='table')



urlpatterns = [
    path('', include(router.urls)),
    path('table-type/',TableTypeView.as_view()),
    path('table-type/<int:pk>/',TableTypeDetailView.as_view())
]