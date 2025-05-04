from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from lessons_app.models import Attendance,Lesson
from .serializers import LessonAttendanceStatsSerializer,CourseTeacherSerializer
from common_app.permissions import *
from rest_framework.permissions import IsAuthenticated
from homework_app.models import *
from django.db.models import Avg
from user_app.models import Student,Teacher





# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from lessons_app.models import Lesson, Attendance

class LessonAttendanceStatsAPIView(APIView):
    permission_classes = [AdminOrOwner]
    """
    O'qituvchining barcha darslari bo'yicha statistikani qaytaradi:
    - dars nomi, sanasi, guruhi
    - umumiy o'quvchilar soni
    - qatnashgan o'quvchilar soni
    - qatnashish foizi (%)
    """
    def get(self, request):
        data = []
        lessons = Lesson.objects.all()

        for lesson in lessons:
            group_students = lesson.group.group_student.all()
            total_students = group_students.count()

            attended_students = Attendance.objects.filter(
                lesson=lesson,
                is_present=True,
                student__in=group_students
            ).count()

            attendance_percentage = (attended_students / total_students) * 100 if total_students else 0

            data.append({
                      "dars_nomi": lesson.title,
                      "dars_sanasi": lesson.lesson_date,
                      "guruh": lesson.group.title,
                      "umumiy_oquvchilar": total_students,
                      "qatnashganlar": attended_students,
                      "foizda_qatnashgan": round(attendance_percentage, 2)
                         })


        return Response(data)

# Dars bo‘yicha uyga vazifalar statistikasi ro‘yxatga qo‘shilyapti Faqat o'qtuvchi uchun 
class LessonHomeworkStatsAPIView(APIView):
    permission_classes = [IsAuthenticated,AdminOrOwner]

    def get(self, request):
        if not hasattr(request.user, 'teacher'):
            return Response({"detail": "Faqat o‘qituvchilar uchun mavjud."}, status=403)

        teacher = request.user.teacher
        lessons = Lesson.objects.filter(teacher=teacher)
        data = []

        for lesson in lessons:
            group = lesson.group
            total_students = group.group_student.count()
            homework = lesson.homeworks.first()

            if homework:
                submitted_answers = HomeworkAnswer.objects.filter(homework=homework)
                submitted_count = submitted_answers.count()
                graded_count = submitted_answers.filter(is_graded=True).count()
                avg_grade = submitted_answers.aggregate(avg=Avg('grade'))['avg'] or 0
            else:
                submitted_count = 0
                graded_count = 0
                avg_grade = 0

            data.append({
    "dars": lesson.title,
    "sana": lesson.lesson_date,
    "guruh": group.title,
    "umumiy_oquvchilar": total_students,
    "topshirilgan_vazifalar": submitted_count,
    "baholangan_vazifalar": graded_count,
    "ortacha_baho": round(avg_grade, 2),
})

        return Response(data)


class TeacherCourseView(APIView):
    permission_classes = [IsAuthenticated,IsAdminOrTeacher]
    def get(self,request,pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return Response({'detail': 'Teaxher bot found!'},status=404)
        course = teacher.course.all()
        serializer = CourseTeacherSerializer(course,many=True)
        return Response(serializer.data,status=200)