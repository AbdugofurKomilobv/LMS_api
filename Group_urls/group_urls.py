from os.path import basename

from rest_framework.routers import DefaultRouter
from django.urls import path, include


from courses_app.views import *

app_name = 'group_url'



router = DefaultRouter()
router.register(r'groups',GroupViewSet, basename='group')


urlpatterns = [
    path('', include(router.urls)),
    path('get-groups-by-ids/',GetGroupByIds.as_view(), name='get-groups-by-ids/')
]