from rest_framework.schemas.coreapi import serializers
from rest_framework.serializers import SerializerMetaclass
from course.models import Course, Material, Picture, Homework, Problem, Choice, Submission, ForumSection, Post
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
        # queryset=Teacher.objects.all(), # type: ignore
        many=True,
        # required=True,
        slug_field="name",
        read_only=True
    )

    students = serializers.SlugRelatedField(
        # queryset=Student.objects.all(), # type: ignore
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


class PictureSerializer(serializers.ModelSerializer):
    material = serializers.StringRelatedField()
    file_path = serializers.ImageField()
    class Meta:
        model = Picture
        fields = [
            "id",
            "file_path",
            "file_name",
            "created_time",
            "material",
        ]
        read_only_fields = [
            "id",
            "file_path",
            "created_time",
            "material",
        ]


class PictureCreateSerializer(serializers.ModelSerializer):
    material = serializers.StringRelatedField()
    class Meta:
        model = Picture
        exclude = ("created_time",)


class HomeworkDetailSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    teacher = serializers.StringRelatedField()
    class Meta:
        model = Homework
        fields = [
            "id",
            "title",
            "course",
            "teacher",
            "view_begin_time",
            "view_end_time",
            "submit_begin_time",
            "submit_end_time",
        ]
        read_only_fields = ["id"]


class HomeworkListSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    teacher = serializers.StringRelatedField()
    class Meta:
        model = Homework
        fields = [
            "id",
            "title",
            "course",
            "teacher",
            "view_begin_time",
            "view_end_time",
            "submit_begin_time",
            "submit_end_time",
        ]
        read_only_fields = ["id"]


class ProblemDetailSerializer(serializers.ModelSerializer):
    teacher = serializers.StringRelatedField()
    homework = serializers.StringRelatedField()
    class Meta:
        model = Problem
        fields = [
            "id",
            "description",
            "points",
            "expected_answer",
            "teacher",
            "homework",
        ]
        read_only_fields = [
            "id",
            "teacher",
            "homework",
        ]


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = [
            "choiceA",
            "choiceB",
            "choiceC",
            "choiceD",
            "is_multiple"
        ]


class SubmissionSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    homework = serializers.StringRelatedField()
    class Meta:
        model = Submission
        fields = [
            "id",
            "student",
            "homework",
            "is_submitted",
            "is_checked",
            "score",
            "remark",
        ]
        read_only_fields = [
            "id",
            "student",
            "homework",
        ]


class ForumSectionSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    class Meta:
        model = ForumSection
        fields = [
            "course",
            "name"
        ]


class PostSerializer(serializers.ModelSerializer):
    section = serializers.SlugRelatedField(
        queryset=ForumSection.objects.all(), # type: ignore
        required=True,
        slug_field="name",
    )
    author = serializers.StringRelatedField()
    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "content",
            "created_at",
            "section"
        ]
        read_only_fields = [
            "id",
            "author",
            "created_at",
        ]
