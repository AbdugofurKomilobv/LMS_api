from django.db.models.signals import post_save
from django.dispatch import receiver
from lessons_app.models import Lesson, Attendance
from user_app.models import Student

@receiver(post_save, sender=Lesson)
def create_attendance_for_lesson(sender, instance, created, **kwargs):
    if created:
        # Lesson yaratilganda guruhdagi barcha studentlar uchun attendance yaratish
        students = instance.group.group_student.all()
        Attendance.objects.bulk_create([
            Attendance(student=student, lesson=instance) for student in students
        ])
