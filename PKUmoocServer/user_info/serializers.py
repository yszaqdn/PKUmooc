from rest_framework import serializers

from user_info.models import (
    User,
    Student,
    Teacher,
)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'is_student', 'is_teacher')
        read_only_fields = ('username', 'is_student', 'is_teacher')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)





class StudentRegisterSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Student
        fields = [
            'name',
            'dept',
            'sex',
            'phone',
            'grade',
        ]

class StudentSerializer(serializers.ModelSerializer):
    
    user = UserSerializer(read_only=True)

    class Meta:
        model = Student
        fields = [
            'user_id',
            'id',
            'name',
            'dept',
            'sex',
            'phone',
            'grade',
            'user',
        ]
        read_only_fields = [
            'user_id',
            'grade',
        ]


class TeacherRegisterSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Teacher
        fields = [
            'name',
            'dept',
            'sex',
            'phone',
        ]


class TeacherSerializer(serializers.ModelSerializer):
    
    user = UserSerializer(read_only=True)

    class Meta:
        model = Teacher
        fields = [
            'user_id',
            'id',
            'name',
            'dept',
            'sex',
            'phone',
            'user',
        ]
        read_only_fields = [
            'user_id',
            'grade',
        ]


class RegisterSerializer(serializers.Serializer):
    id = serializers.CharField(label="学号")
    password = serializers.CharField(label="密码")
    confirmpassword = serializers.CharField(label="确认密码")
    email = serializers.EmailField(label="邮箱")
    phone = serializers.IntegerField(label="电话号码")
    name = serializers.CharField(label="姓名")
    sex = serializers.CharField(label="性别")
    dept = serializers.CharField(label="学院")
    identity = serializers.CharField(label="身份")
    grade = serializers.IntegerField(label="年级", required=False)

