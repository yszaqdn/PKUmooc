from rest_framework import serializers

from user_info.models import User
from user_info.models import Teacher
from user_info.models import Student


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_student', 'is_teacher')


class StudentSerializer(serializers.ModelSerializer):
    dept = serializers.StringRelatedField()
    class Meta:
        model = Student
        fields = ('name', 'id', 'dept', 'grade', 'phone', 'sex')


class TeacherSerializer(serializers.ModelSerializer):
    dept = serializers.StringRelatedField()
    class Meta:
        model = Teacher
        fields = ('name', 'id', 'dept', 'phone', 'sex')
