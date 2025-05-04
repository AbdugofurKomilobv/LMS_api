from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from lessons_app.models import Lesson, Attendance
from lessons_app.serializers import LessonSerializer, AttendanceSerializer,StudenGrouptSerializer,AttendanceStudentMeSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from common_app.permissions import AdminOrTeacher
from user_app.models import Student
from rest_framework.generics import get_object_or_404

class CreateLessonView(APIView):
    permission_classes = [IsAuthenticated,AdminOrTeacher]

    @swagger_auto_schema(
        operation_description="Create a new lesson",
        request_body=LessonSerializer,
        responses={201: LessonSerializer, 400: "Invalid data"}
    )
    def post(self, request):
        # `request`ni serializerga kontekstdan uzatish
        serializer = LessonSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            lesson = serializer.save()  # Yangi dars yaratish
            return Response(LessonSerializer(lesson).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class AttendanceListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all attendance records for a lesson",
        responses={200: AttendanceSerializer(many=True)}
    )
    def get(self, request, lesson_id):
        attendance = Attendance.objects.filter(lesson_id=lesson_id)
        serializer = AttendanceSerializer(attendance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AttendanceUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update attendance for a lesson",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'attendance': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'student_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the student"),
                            'is_present': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Attendance status")
                        }
                    )
                )
            }
        ),
        responses={200: "Attendance updated successfully", 400: "Invalid data"}
    )
    def post(self, request, lesson_id):
        attendance_data = request.data.get('attendance', [])  # Default to empty list if 'attendance' key is missing
        for entry in attendance_data:
            student = Student.objects.get(id=entry['student_id'])
            attendance, created = Attendance.objects.update_or_create(
                lesson_id=lesson_id,
                student=student,
                defaults={'is_present': entry['is_present']}
            )
        return Response({"status": "Davomat muvaffaqiyatli yangilandi"}, status=status.HTTP_200_OK)

class LessonListView(APIView):
    permission_classes = [IsAuthenticated,AdminOrTeacher]

    def get(self, request, group_id):
        # Guruh ID bo'yicha barcha darslarni filtrlaymiz
        lessons = Lesson.objects.filter(group_id=group_id)
    

        if not lessons:
            return Response({"detail": "Bu guruhda darslar mavjud emas."}, status=status.HTTP_404_NOT_FOUND)

        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# Teacher o'ziga tegishli guruxlarni o'quvchilarini korish
class GroupStudentsView(APIView):
    permission_classes = [IsAuthenticated, AdminOrTeacher]

    @swagger_auto_schema(
        operation_description="Get all students in a group",
        responses={200: StudenGrouptSerializer(many=True)}
    )
    def get(self, request, group_id):
        students = Student.objects.filter(group=group_id)
        if not students.exists():
            return Response({"detail": "Bu guruhda oquvchilar yoq."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StudenGrouptSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# student o'zini davomatlarini korish
class StudentAttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student = request.user.student  # `User`dan `Student` obyektini olamiz
        attendance_qs = Attendance.objects.filter(student=student)
        serializer = AttendanceStudentMeSerializer(attendance_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)