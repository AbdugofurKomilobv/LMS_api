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
            return Response({"message": "Superadmin yaratildi"},status=201)
        return Response(serializer.errors,status=400)
    

# Barcha userlarni korish
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserAllSerializer
    pagination_class  = Pagination
    permission_classes = [AdminUser]


# Userni id boyicha qidirish
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserAllSerializer
    lookup_field = 'id'
    permission_classes = [AdminUser]

# Oddiy user yaratish
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserAllSerializer
    permission_classes = [AdminUser]

# Userni taxrirlash malumotlarni yangilash
class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserAllSerializer
    lookup_field = 'id'
    permission_classes = [AdminUser]

# Userni o'chirish
class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserAllSerializer
    lookup_field = 'id'
    permission_classes = [AdminUser]


# ==================================================


# Teacher

# Barcha ustozlarni korish
class TeacherListView(ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    pagination_class = Pagination
    permission_classes = [AdminUser]

# Ustozni malumotlarni yangiyash
class TeacherUpdateView(UpdateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    lookup_field = 'id'
    permission_classes = [AdminUser]

class TeacherRetrieveAPIView(RetrieveAPIView):
    """
    ID orqali bitta Teacher ma'lumotini olish uchun API.
    Faqat Admin yoki o'z profili egasi ko'rishi mumkin.
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    lookup_field = 'id'
    permission_classes = [AdminOrOwner]


# Bir nechta ustozlarni id si orqali olish
class GetTeacherByIds(APIView):
    permission_classes = [AdminUser]
    
    @swagger_auto_schema(request_body=GetTeachersByIdsSerializer)
    def post(self, request):
        teacher_ids = request.data.get('teacher_ids', [])
        
        # Tekshirish: teacher_ids ro'yxati bo'lishi kerak
        if not teacher_ids or not isinstance(teacher_ids, list):
            return Response({"error": "teacher_ids ro‘yxati bo‘lishi kerak"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Teacherlarni id'lari bo'yicha filtrlaymiz
        teachers = Teacher.objects.filter(id__in=teacher_ids)
        
        # Teacherlarni serializatsiya qilamiz
        serializer = TeacherSerializer(teachers, many=True)
        
        # Javob qaytarish
        return Response({"teachers": serializer.data}, status=status.HTTP_200_OK)

# O'qtuvchi yaratish
class TeacherCreateView(APIView):
    permission_classes = [AdminUser]
    @swagger_auto_schema(request_body=UserAndTeacherserializer)
    def post(self, request):
         user_data = request.data.get('user', {})
         user_serializer = UserSerializer(data=user_data)

         if not user_serializer.is_valid():
             return Response(user_serializer.errors, status=400)

         user = user_serializer.save(is_teacher=True)

         teacher_data = request.data.get('teacher', {})
         teacher_serializer = TeacherSerializer(data=teacher_data)

         if not teacher_serializer.is_valid():
             user.delete()
             return Response(teacher_serializer.errors, status=400)

         teacher_serializer.save(user=user)
         return Response(teacher_serializer.data, status=201)

# O'qtuvchini id si orqali qaysi guruxga biriktirilganligini korish
class TeacherGrouView(APIView):
    permission_classes = [AdminOrOwner]

    def get(self,request,teacher_id):
        try:
            teacher = Teacher.objects.get(id=teacher_id)
        except Teacher.DoesNotExist:
            return Response({"error": "Teacher not found"}, status=404)
        
        groups = teacher.groups.all()
        serializer = GroupSerializer(groups,many=True)

        return Response(serializer.data,status=200)

class TeacherGroupDetailAPIView(APIView):
    permission_classes = [IsAuthenticated,AdminOrTeacher]
     
    def get(self,request,teacher_id,group_id):
        if not request.user.is_admin and (
            not hasattr(request.user, 'teacher') or request.user.teacher.id  != teacher_id):
            return Response({'detail':"Siz faqat o'zingizni guruxingizni ko'raolasiz "},status=403)
        
        try:
            # o'qtuvchiga tegishli guruxni izlash
            group = Group.objects.get(id = group_id,teacher__id=teacher_id)
            students = Student.objects.filter(group=group)

            group_data = GroupSerializer(group).data
            students_data = StudentSerializer(students,many=True).data

            return Response({
                'group_data':group_data,
                'students_data':students_data,
            
            },status=200)
        except Group.DoesNotExist:
            return Response({"detail": "Guruh topilmadi yoki bu o'qituvchiga tegishli emas."}, status=status.HTTP_404_NOT_FOUND)
        
        
# =========================================================



