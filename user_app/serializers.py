from rest_framework import serializers

from django.contrib.auth.hashers import make_password

from courses_app.models import Group,Course
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
        fields = ('id','user',"course",'description')

    

# ======================================================================

class S_UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['phone','full_name','password']
class StudentCreateSerializer(serializers.ModelSerializer):
    user = S_UserSerializer()
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True, required=False)

    class Meta:
        model = Student
        fields = ['user', 'groups', "course", 'description']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        courses = validated_data.pop('course', [])
        groups = validated_data.pop('groups', [])
         
        password = user_data.get('password')
        if not password:
            raise serializers.ValidationError({"password": "Password majburiy."})
        
        user_data_copy = user_data.copy()
        user_data_copy.pop('password')

        user = User.objects.create(**user_data, is_student=True)
        user.set_password(password)
        user.save()

        student = Student.objects.create(user=user, **validated_data)
        student.group.set(groups)  # Grouplarni to'g'ri qo'shish
        student.course.set(courses)
        return student

# ==================================

class StudentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Student
        fields = ('id','user','group', 'course', 'description')


class ParentSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True,read_only=True)

    class Meta:
        model = Parent
        fields = ('id','name','surname','phone','description','students')

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


