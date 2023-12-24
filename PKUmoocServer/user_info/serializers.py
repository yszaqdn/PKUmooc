from rest_framework import serializers

from user_info.models import (
    User,
    Student,
    Teacher,
    Dept,
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


class DeptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dept
        fields = [
            'id',
            'name',
        ]


class StudentRegisterSerializer(serializers.ModelSerializer):
    dept = serializers.PrimaryKeyRelatedField(queryset=Dept.objects.all())
    
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
    dept = serializers.StringRelatedField()
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
    dept = serializers.PrimaryKeyRelatedField(queryset=Dept.objects.all())

    class Meta:
        model = Teacher
        fields = [
            'name',
            'dept',
            'sex',
            'phone',
        ]


class TeacherSerializer(serializers.ModelSerializer):
    dept = serializers.StringRelatedField()
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
