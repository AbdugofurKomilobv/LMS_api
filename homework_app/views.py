from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from homework_app.models import Homework
from homework_app.serializers import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.generics import ListAPIView,ListCreateAPIView,RetrieveAPIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

class HomeworkCreateAPIView(CreateAPIView):
    queryset = Homework.objects.all()
    serializer_class = HomeworkCreateSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Homework qo‘shish (faqat teacher)",
        operation_description="Ustoz o‘ziga tegishli darsga homework yaratadi.",
        request_body=HomeworkCreateSerializer,
        responses={201: HomeworkCreateSerializer()}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    

class HomeworkAnswerListAPIView(ListAPIView):
    serializer_class = HomeworkAnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        teacher = self.request.user.teacher
        homework_id = self.kwargs['homework_id']

        return HomeworkAnswer.objects.filter(
            homework__id=homework_id,
            homework__lesson__teacher=teacher
        )
    @swagger_auto_schema(
        operation_summary="Uyga vazifaga yozilgan barcha javoblarni ko‘rish (Faqat Teacher koradi)",
        operation_description="Faqat shu homework o‘ziga tegishli bo‘lsa, ustoz o‘quvchilarning javoblarini ko‘ra oladi."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class HomeworkAnswerGradeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Homework javobini baholash",
        operation_description="Ustoz o'quvchining homework javobini baholaydi.",
        request_body=HomeworkAnswerSerializer,
        responses={200: HomeworkAnswerSerializer}
    )
    def post(self, request, homework_answer_id):
        teacher = request.user.teacher
        homework_answer = HomeworkAnswer.objects.filter(id=homework_answer_id).first()

        if not homework_answer:
            return Response({'detail': 'Javob topilmadi.'}, status=404)

        # Check if the homework is for the teacher's lesson
        if homework_answer.homework.lesson.teacher != teacher:
            return Response({'detail': 'Siz bu homework javobini baholay olmaysiz.'}, status=403)

        # Update grade and is_graded status
        serializer = HomeworkAnswerSerializer(homework_answer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(is_graded=True)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

# ================================================================
# Student uchun


class StudentHomeworkListAPIView(ListAPIView):
    serializer_class = StudentHomeworkListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
       student = self.request.user.student
       return Homework.objects.filter(group__in=student.group.all())









class StudentHomeworkAnswerAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=StudentHomeworkAnswerSerializer,
        responses={201: StudentHomeworkAnswerSerializer()}
    )
    def post(self, request, homework_id):
        student = request.user.student
        data = request.data.copy()
        data['homework'] = homework_id
        data['student'] = student.id

        serializer = StudentHomeworkAnswerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


      
# views.py - O'quvchining javobi va bahosini ko'rish
class StudentBaxosikAnswerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, homework_id):
        # Tizimga kirgan foydalanuvchi o'quvchi ekanligini tekshiramiz
        try:
            student = request.user.student
        except AttributeError:
            return Response({'detail': 'Foydalanuvchi o\'quvchi emas.'}, status=400)

        # HomeworkAnswer modelidan studentning javobini qidiramiz
        homework_answer = HomeworkAnswer.objects.filter(homework_id=homework_id, student=student).first()

        if homework_answer:
            # Agar javob topilsa, javob va baho haqida ma'lumotlarni yuboramiz
            serializer = HomeworkAnswerSerializer(homework_answer)
            return Response(serializer.data)
        else:
            # Agar javob yuborilmagan yoki tekshirilmagan bo'lsa, xato xabarini qaytaramiz
            return Response({'detail': 'Javob hali yuborilmagan yoki tekshirilmagan.'}, status=404)
        


class StudentGradedHomeworkAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Tizimga kirgan foydalanuvchi o'quvchi ekanligini tekshiramiz
        try:
            student = request.user.student
        except AttributeError:
            return Response({'detail': 'Foydalanuvchi o\'quvchi emas.'}, status=400)

        # O'quvchining barcha baxolangan homework javoblarini qidiramiz
        graded_homeworks = HomeworkAnswer.objects.filter(student=student, is_graded=True)

        # Agar baxolangan homeworklar mavjud bo'lsa, ularni serializer orqali yuboramiz
        if graded_homeworks.exists():
            serializer = HomeworkAnswerSerializer(graded_homeworks, many=True)
            return Response(serializer.data)
        else:
            # Agar baxolangan homeworklar topilmasa, xato xabarini qaytaramiz
            return Response({'detail': 'Hali baxolangan homeworklar mavjud emas.'}, status=404)
