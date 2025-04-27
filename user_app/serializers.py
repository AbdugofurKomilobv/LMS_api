from rest_framework import serializers

from django.contrib.auth.hashers import make_password

from courses_app.models import Group
from user_app.models import Teacher,User,Student,Parent

class UserAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

# =======================================================================
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","password","full_name","phone")

    def create(self,validated_data):
            validated_data['password'] = make_password(validated_data['password'])
            return super().create(validated_data)

# ========================================================================

class TeacherSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only = True)
    class Meta:
        model = Teacher
        fields = ('id','user',"cource",'description')



# ======================================================================


class StudentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Student
        fields = ('id','user','group', 'cource', 'description')


class ParentSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True,read_only=True)

    class Meta:
        model = Parent
        fields = ('id','name','surname','address','phone','description','students')

# =======================================================================


class SuperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone','password','full_name']
        extra_kwargs = {'password':{'write_only':True}}

    def create(self,validates_data):
        return User.objects.create_superuser(**validates_data)
    
# ===================================================


class GetStudentByIdSerializer(serializers.Serializer):
    student_ids = serializers.ListField(child = serializers.IntegerField())


class GetTeachersByIdsSerializer(serializers.Serializer):
    teacher_ids = serializers.ListField(child=serializers.IntegerField())


class  UserAndTeacherserializer(serializers.Serializer):
    user = UserSerializer()
    teacher = TeacherSerializer()

class UserAndStudentSerializer(serializers.Serializer):
    user = UserSerializer()
    student = StudentSerializer()
    parent = ParentSerializer()


