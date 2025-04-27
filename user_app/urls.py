from django.urls import path, include
from rest_framework.routers import DefaultRouter


from user_app.views import CreateSuperuserView


app_name = 'users'

urlpatterns = [
    # createsuperuser
    path('create/superuser',CreateSuperuserView.as_view(),name='create-superuser')
]