from rest_framework import serializers
from lessons_app.models import Lesson, Attendance
from user_app.models import Student,Teacher
from homework_app.models import *
class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    class Meta:
        model = Attendance
        fields = ['student', 'student_name', 'lesson','lesson_title', 'is_present', 'timestamp']





class LessonSerializer(serializers.ModelSerializer):
    group_title = serializers.CharField(source='group.title', read_only=True)

    class Meta:
        model = Lesson
        fields = ['id','title', 'group', 'lesson_date', 'description', 'group_title']

    def create(self, validated_data):
        group = validated_data.get('group')
        user = self.context['request'].user  # Hozirgi autentifikatsiyalangan foydalanuvchi

        # Teacher modelidan hozirgi foydalanuvchi asosida teacherni olish
        try:
            teacher = Teacher.objects.get(user=user)
        except Teacher.DoesNotExist:
            raise serializers.ValidationError("Siz ushbu guruh uchun dars yaratish huquqiga ega emassiz.")

        # Ustozni guruhga biriktirilganligini tekshirish
        if not group.teacher.filter(id=teacher.id).exists():
            raise serializers.ValidationError("Siz ushbu guruh uchun dars yaratish huquqiga ega emassiz.")
        
        # Lesson yaratish
        lesson = Lesson.objects.create(
            teacher=teacher,  # Darsni teacher bilan yaratamiz
            **validated_data
        )
        return lesson

class StudenGrouptSerializer(serializers.ModelSerializer):
     full_name = serializers.CharField(source='user.full_name', read_only=True)

     class Meta:
        model = Student
        fields = ['id', 'full_name'] 






class AttendanceStudentMeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    homework_mark = serializers.SerializerMethodField()
    homework_comment = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = [
            'student', 'student_name',
            'lesson', 'lesson_title',
            'is_present',
            'homework_mark', 'homework_comment'
        ]
    
    

    
    def get_homework_mark(self, obj):
        answer = HomeworkAnswer.objects.filter(homework__lesson=obj.lesson, student=obj.student).first()
        return answer.grade if answer else None

    def get_homework_comment(self, obj):
        answer = HomeworkAnswer.objects.filter(homework__lesson=obj.lesson, student=obj.student).first()
        return answer.answer_text if answer else None
