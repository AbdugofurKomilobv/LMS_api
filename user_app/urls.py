from django.urls import path, include
from rest_framework.routers import DefaultRouter


from user_app.views import CreateSuperuserView,UserListView,UserDetailView,UserCreateView,UserUpdateView,UserDeleteView


app_name = 'users'

urlpatterns = [
    # createsuperuser
    path('create/superuser',CreateSuperuserView.as_view(),name='create-superuser'),
    # users
    path('',UserListView.as_view(),name='user-list'),
    path('user/<int:id>/', UserDetailView.as_view(), name='user-detail'), 
    path('create/user/', UserCreateView.as_view(), name='user-create'), 
    path('update/user/<int:id>/', UserUpdateView.as_view(), name='user-update'), 
    path('delete/user/<int:id>/', UserDeleteView.as_view(), name='user-delete'),

]