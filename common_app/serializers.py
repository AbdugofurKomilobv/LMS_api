from collections import Counter
from rest_framework import serializers
from lessons_app.models import Lesson, Attendance
from user_app.models import Student,Teacher


class LessonAttendanceStatsSerializer(serializers.Serializer):
    lesson_title = serializers.CharField(source='lesson.title')
    total_students = serializers.IntegerField()
    present_count = serializers.IntegerField()
    absent_count = serializers.IntegerField()

    def to_representation(self, instance):
        lesson = instance.lesson
        total_students = lesson.students.count()  # Barcha o'quvchilar
        attendance_data = Attendance.objects.filter(lesson=lesson)
        attendance_count = Counter([attendance.is_present for attendance in attendance_data])

        return {
            'lesson_title': lesson.title,
            'total_students': total_students,
            'present_count': attendance_count.get(True, 0),
            'absent_count': attendance_count.get(False, 0),
        }
