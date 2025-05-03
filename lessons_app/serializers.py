from rest_framework import serializers
from lessons_app.models import Lesson, Attendance
from user_app.models import Student,Teacher

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)

    class Meta:
        model = Attendance
        fields = ['student', 'student_name', 'lesson', 'is_present', 'timestamp']





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




