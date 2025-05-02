from rest_framework import serializers
from lesson_app.models import *






class AttendanceInlineSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=['kelgan', 'kelmagan', 'sababli'])


class LessonCreateSerializer(serializers.ModelSerializer):
    attendances = AttendanceInlineSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ['title', 'group', 'teacher', 'date', 'description', 'attendances']

    def create(self, validated_data):
        attendances_data = validated_data.pop('attendances')
        lesson = Lesson.objects.create(**validated_data)

        attendance_objects = []
        student_ids = [att['student_id'] for att in attendances_data]

        # Darsga tegishli barcha o'quvchilarni olish
        students_in_group = Student.objects.filter(group=lesson.group)

        # O'quvchilarni tekshirib, kelgan yoki kelmagan holatlarini belgilash
        for student in students_in_group:
            status = "kelgan" if student.id in student_ids else "kelmagan"
            attendance_objects.append(Attendance(
                lesson=lesson,
                student=student,
                status=status
            ))

        # Attendance ob'ektlarini bazaga saqlash
        Attendance.objects.bulk_create(attendance_objects)
        return lesson


class AttendanceDisplaySerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='student.user.full_name')
    phone = serializers.CharField(source='student.user.phone')

    class Meta:
        model = Attendance
        fields = ['id', 'full_name', 'phone', 'status']


