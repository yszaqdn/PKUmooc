from rest_framework.schemas.coreapi import serializers
from course.models import Course, Material
from user_info.models import Student, Teacher
from rest_framework.fields import SerializerMethodField


class CourseDetailSerializer(serializers.ModelSerializer):
    teachers = serializers.SlugRelatedField(
        # queryset=Teacher.objects.all(),
        many=True,
        # required=True,
        slug_field="name",
        read_only=True,
    )

    students = serializers.SlugRelatedField(
        # queryset=Student.objects.all(),
        many=True,
        # required=False,
        slug_field="name",
        read_only=True,
    )

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "year",
            "session",
            "teachers",
            "students",
        ]
        read_only_fields = [
            "id",
        ]



class CourseListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="course:course-detail")

    teachers = serializers.SlugRelatedField(
        queryset=Teacher.objects.all(), # type: ignore
        many=True,
        required=True,
        slug_field="name"
    )

    students = serializers.SlugRelatedField(
        queryset=Student.objects.all(), # type: ignore
        many=True,
        required=False,
        slug_field="name"
    )

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "year",
            "session",
            "url",
            "teachers",
            "students",
        ]


class MaterialDetailSerializer(serializers.ModelSerializer):
    teacher = serializers.StringRelatedField()
    course = serializers.StringRelatedField()

    class Meta:
        model = Material
        fields = [
            "id",
            "title",
            "teacher",
            "course",
            "updated_time",
            "is_public",
            "content",
        ]
        read_only_fields = [
            "id",
            "updated_time",
        ]


class MaterialListSerializer(serializers.ModelSerializer):
    teacher = serializers.StringRelatedField()
    course = serializers.StringRelatedField()

    class Meta:
        model = Material
        fields = [
            "id",
            "title",
            "teacher",
            "course",
            "updated_time",
            "is_public",
        ]
        read_only_fields = [
            "id",
            "updated_time",
        ]
