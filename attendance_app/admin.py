from django.contrib import admin



from attendance_app.models import Status, Attendance

admin.site.register([Status,Attendance])
