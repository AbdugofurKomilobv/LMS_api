from calendar import month_name
from collections import defaultdict

from drf_yasg import openapi
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,UpdateAPIView,RetrieveAPIView,get_object_or_404
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from drf_yasg.utils import swagger_auto_schema


from attendance_app.models import Attendance
from attendance_app.serializers import AttendanceSerializer
from common_app.permissions import AdminUser, AdminOrOwner, AdminOrTeacher, AdminOrStudent
from common_app.pagination import Pagination, StudentAttendancePagination

from courses_app.models import Group
from courses_app.serializers import GroupSerializer
from user_app.serializers import TeacherSerializer, UserSerializer, StudentSerializer, UserAndTeacherserializer, \
    UserAndStudentSerializer, ParentSerializer, UserAllSerializer, GetStudentByIdSerializer, \
    GetTeachersByIdsSerializer, SuperUserSerializer
from user_app.models import Teacher,Student,User,Parent



# User

# Supperuser yaratish
class CreateSuperuserView(APIView):
    permission_classes = [AdminUser]

    @swagger_auto_schema(request_body=SuperUserSerializer)
    def post(self,request):
        serializer = SuperUserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Superadmin successfully created"},status=201)
        return Response(serializer.errors,status=400)
