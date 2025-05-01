from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView



from courses_app.models import Group,Course,Table,TableType
from common_app.permissions import AdminOrOwner,AdminOrStudent,AdminOrTeacher,AdminUser
from common_app.pagination import Pagination
from courses_app.serializers import GroupSerializer, GroupAddStudent, GroupAddTeacher, \
    CourseSerializer, TableSerializer, TableTypeSerializer, RemoveStudentFromGroupSerializer, \
    RemoveTeacherFromGroupSerializer, \
    GetGroupByIdsSerializer
from user_app.models import Teacher,Student



class GroupViewSet(viewsets.ViewSet):
    permission_classes = [AdminUser]

    # bu funcsiya barcha guruxlarni bazadan oladi
    def list(self,request):
        groups = Group.objects.all()
        paginator = Pagination()
        result_pages =paginator.paginate_queryset(groups,request)
        serializer = GroupSerializer(result_pages,many = True)
        return Response(serializer.data)
    

    # retrieve bu guruxni id siga qarab oladi 
    def retrieve(self,request,pk=None):
        group = get_object_or_404(Group,pk=pk)
        serilizer = GroupSerializer(group)
        return Response(serilizer.data)
    

   # Bu action faqat 'POST' so'rovini qabul qiladi va URL yo'li '/create/group' bo'ladi.
    @action(detail=False,methods=['post'],url_path='crate/group')
    # Yangi gurux yaratish 
    @swagger_auto_schema(request_body=GroupSerializer)
    def create_group(self,request):
        serializer = GroupSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)
    # ======================================================================


    # Gurux malumotlarini yangilash
    @action(detail=True,methods=['put'],url_path='update/group')
    @swagger_auto_schema(request_body=GroupSerializer)
    def update_group(self,request,pk=None):
        group = get_object_or_404(Group,pk=pk)
        serializer = GroupSerializer(group,data = request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors,status=400)
    # ============================================================================



    # Gruxni o'chirish
    @action(detail=True,methods=['delete'],url_path='delete/group')
    def delete_group(self,request,pk=None):
        group = get_object_or_404(Group,pk=pk)
        group.delete()
        return Response({"success":True,
                         'detail': "Gurux muaffaqyatli o'chirildi"},status=204)
    
    # ============================================================================

    
    # student qoshish guruxga
    @action(detail=True,methods=['post'],url_path='add-student')
    @swagger_auto_schema(request_body=GroupAddStudent)
    def add_student(self,request,pk=None):
        group = get_object_or_404(Group,pk=pk)
        serializer = GroupAddStudent(data = request.data)

        if serializer.is_valid():
            student_id = serializer.validated_data['student_id']
            student = get_object_or_404(Student,pk = student_id)
            student.group.add(group)
            student.save()
            return Response({'status':True,'detail': f'Student {student.user.full_name} - guruhga qushildi {group.title}'},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,status=400)
    
    # ============================================================================

    # Studentni guruxdan chiqarish
    @action(detail=True, methods=['post'], url_path='remove-student')
    @swagger_auto_schema(request_body=RemoveStudentFromGroupSerializer)
    def remove_student(self, request, pk=None):
    # Guruhni olish
      group = get_object_or_404(Group, pk=pk)
    
    # Serializerni ishlatish
      serializer = RemoveStudentFromGroupSerializer(data=request.data)

    # Serializerni tekshirish
      if serializer.is_valid():
        student_id = serializer.validated_data['student_id']
        
        try:
            # Studentni olish
            student = Student.objects.get(id=student_id)

            # Agar student guruhga tegishli bo'lsa
            if student.group.filter(id=group.id).exists():
                student.group.remove(group)
                return Response({"status": True, "detail": f"Student {student.user.full_name} - guruhdan chiqarildi."}, status=200)
            
            return Response({"status": False, "detail": "Bu student ushbu guruhga tegishli emas."}, status=400)

        except Student.DoesNotExist:
            # Student topilmasa
            return Response({"status": False, "detail": "Student topilmadi."}, status=404)
    
    # Agar serializer noto'g'ri bo'lsa
      return Response({"status": False, "detail": serializer.errors}, status=400)
    


    # =============================================================================================



    # guruxga O'qtuvchi qo'shoish 
    @action(detail=True, methods=['post'], url_path='add-teacher')
    @swagger_auto_schema(request_body=GroupAddTeacher)
    def add_teacher(self, request, pk=None):
         group = get_object_or_404(Group, pk=pk)
         serializer = GroupAddTeacher(data=request.data)

         if serializer.is_valid():
           teacher_id = serializer.validated_data['teacher_id']
        
           try:
            teacher = Teacher.objects.get(id=teacher_id)

            if teacher.groups.filter(id=group.id).exists():
                return Response(
                    {'status': False, 'detail': f'Teacher {teacher.user.phone} - allaqachon {group.title} guruhida mavjud.'},
                    status=status.HTTP_400_BAD_REQUEST)
            
            teacher.groups.add(group)
            teacher.save()

            return Response(
                {'status': True, 'detail': f'Teacher {teacher.user.phone} - guruhga qo\'shildi: {group.title}'},
                status=status.HTTP_200_OK)
        
           except Teacher.DoesNotExist:
            return Response({'status': False, 'detail': 'Teacher topilmadi.'}, status=status.HTTP_404_NOT_FOUND)
    
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # =====================================================================================


    # O'qtuvchini guruxdan chiqarish
    @action(detail=True, methods=['post'], url_path='remove-teacher')
    @swagger_auto_schema(request_body=RemoveTeacherFromGroupSerializer,)
    def remove_teacher(self, request,pk=None):
        group = get_object_or_404(Group, pk=pk)
        teacher_id = request.data.get("teacher_id")

        if not teacher_id:
            return Response({"status": False, "detail": "teacher_id kerak"}, status=400)
        try:
            teacher = Teacher.objects.get(id=teacher_id)

            if teacher.groups.filter(id=group.id).exists():
                teacher.groups.remove(group)
                return Response({"status": True, "detail": f"Teacher {teacher.user.full_name} - guruhdan chiqarildi."},
                                status=200)
            return Response({"status": False, "detail": "Bu teacher ushbu guruhda mavjud emas."}, status=400)

        except Student.DoesNotExist:
            return Response({"status": False, "detail": "Teacher topilmadi."}, status=404)
        

        # ======================================================================================


class GetGroupByIds(APIView):
    permission_classes = [AdminUser]

    @swagger_auto_schema(request_body=GetGroupByIdsSerializer)
    def post(self, request):
        # Foydalanuvchidan group_ids ro'yxatini olish
        group_ids = request.data.get("group_ids", [])

        # group_ids bo'sh yoki ro'yxat emasligini tekshirish
        if not group_ids or not isinstance(group_ids, list):
            return Response({"error": "group_ids ro‘yxati bo‘lishi kerak"}, status=status.HTTP_400_BAD_REQUEST)

        # Berilgan group_ids bo'yicha guruhlarni topish
        groups = Group.objects.filter(id__in=group_ids)

        # Guruhlarni serializatsiya qilish
        serializer = GroupSerializer(groups, many=True)

        # Javobni qaytarish
        return Response({"groups": serializer.data}, status=status.HTTP_200_OK)













# Subject



# Course 
class CourseViewSet(viewsets.ViewSet):
    permission_classes = [AdminUser]
     

    # Barcha kurslarni korish
    def list(self,request):
        courses = Course.objects.all()
        paginator = Pagination()
        result_page = paginator.paginate_queryset(courses,request)
        serializer = CourseSerializer(result_page,many=True)
        return Response(serializer.data)
    def retrieve(self,request,pk=None):
        course = get_object_or_404(Course,pk=pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    
    # Kurs yaratish 
    @action(detail=False,methods=['post'],url_path='create/course')
    @swagger_auto_schema(request_body=CourseSerializer)
    def create_course(self,request):
        serializer = CourseSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":True,"detail": "Kurs muoffaqyatli yaratildi", "course":serializer.data},status=201)
        return Response(serializer.errors, status=400)
    
    # Kursni update qilish taxrirlash degani
    @action(detail=True,methods=['put'],url_path='update/course')
    @swagger_auto_schema(request_body=CourseSerializer)
    def update_course(self,request,pk =None):
        course = get_object_or_404(Course,pk=pk)
        serializer = CourseSerializer(course,data=request.data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":True,"detatil": "Kurs muoffaqyatli taxrirlandi","course":serializer.data},status=200)
        return Response(serializer.errors,status=400)
    

    # Kursni o'chirish
    @action(detail=True,methods=['delete'],url_path='delete/course')
    def delete_course(self,request,pk =None):
        course = get_object_or_404(Course,pk=pk)
        course.delete()
        return Response({"status":True,"detatil":"Kurs o'chirildi"},status=204)
    

# ===============================================================================================

# Table
class TableViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    # barcha jadvalni korish
    def list(self, request):
        tables = Table.objects.all()
        paginator = Pagination()
        result_page = paginator.paginate_queryset(tables, request)
        serializer = TableSerializer(result_page, many=True)
        return Response(serializer.data)
    
    # id si  orqali jadvalni qidirish ko'rish
    def retrieve(self,request,pk=None):
        table = get_object_or_404(Table,pk=pk)
        serializer = TableSerializer(table)
        return Response(serializer.data)
    

    # yangi table yaratish
    @action(detail=False,methods=['post'],url_path='create/table')
    @swagger_auto_schema(request_body=TableSerializer)
    def create_table(self,request):
        serializer = TableSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":True,"detail":"Table yaratildi", "table": serializer.data},status=201)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # tableni taxririlash
    @action(detail=True,methods=['put'],url_path='update/table')
    @swagger_auto_schema(request_body=TableSerializer)
    def update_table(self,request,pk=None):
        table = get_object_or_404(Table,pk=pk)
        serializer = TableSerializer(table,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":True,"detail": "Jadval taxrirlandi","table": serializer.data},status=200)
        return Response(serializer.errors,status=400)
    
    # table ni o'chirish
    @action(detail=True,methods=['delete'],url_path='delete/table')
    def delete_table(self,request,pk=None):
        table = get_object_or_404(Table,pk=pk)
        table.delete()
        return Response({'status':True,'detail': 'Table muaffaqiyatli uchirildi'}, status=status.HTTP_204_NO_CONTENT)

# ===========================================================================================================






    

    









   

    

    