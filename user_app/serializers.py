from rest_framework import serializers

from django.contrib.auth.hashers import make_password

from courses_app.models import Group
from user_app.models import Teacher,User,Student,Parent

class UserAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"