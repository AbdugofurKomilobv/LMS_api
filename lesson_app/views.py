from django.shortcuts import render
from rest_framework.generics import CreateAPIView,RetrieveAPIView,ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from common_app.permissions import *

from lesson_app.serializer import *

from user_app.models import Teacher





# Lesson yaratib kegan kemagan o'quvchilarni belgilash
class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonCreateSerializer
    permission_classes = [IsAdminOrTeacher]  

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lesson = serializer.save()  # Bu yerda Lesson obyekt yaratiladi
        headers = self.get_success_headers(serializer.data)

        attendances = Attendance.objects.filter(lesson=lesson)
        students = [
            {
                "full_name": attendance.student.user.full_name,
                "phone": attendance.student.user.phone,
                "status": attendance.status
            }
            for attendance in attendances
        ]
        # Custom javob
        return Response({
            "message": "Lesson successfully created",
            "lesson_id": lesson.id,
            "title": lesson.title,
            "date": lesson.date,
            "group": lesson.group.id,
            "teacher": lesson.teacher.id if lesson.teacher else None,
            "students": students
          
        },)



# gururx id va lesson id orqali lessonlarni ko'rish faqat admin yoki uwa gurux ustozi uchun
class LessonDetailAPIView(APIView):
    permission_classes = [IsAdminOrTeacher] 

    def get(self, request, lesson_id, group_id):
        # Guruhni topish
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=404)

        # Darsni topish
        try:
            lesson = Lesson.objects.get(id=lesson_id, group=group)
        except Lesson.DoesNotExist:
            return Response({"error": "Lesson not found in the specified group"}, status=404)

        # Darsga tegishli o'quvchilarni olish
        attendances = Attendance.objects.filter(lesson=lesson)
        students = [
            {
                 
                'full_name': attendance.student.user.full_name,
                'phone': attendance.student.user.phone,
                'status': attendance.status
            }
            for attendance in attendances
        ]

        # Natijani qaytarish
        return Response({
             'lesson_id': lesson.id,
            'lesson_title': lesson.title,
            'group_title': group.title,
            'date': lesson.date,
            'students': students
        })



