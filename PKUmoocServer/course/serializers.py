from rest_framework.schemas.coreapi import serializers
from course.models import Course
from user_info.models import Student, Teacher


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
        queryset=Teacher.objects.all(),
        many=True,
        required=True,
        slug_field="name"
    )

    students = serializers.SlugRelatedField(
        queryset=Student.objects.all(),
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

