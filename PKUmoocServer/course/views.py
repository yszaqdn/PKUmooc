from rest_framework.response import Response
from rest_framework.schemas.coreapi import serializers
from course.models import Course
from rest_framework.views import APIView, status
from rest_framework.decorators import api_view
from PKUmoocServer.settings import BASE_DIR
import os
from django.utils import timezone
from course.permissions import IsTeacherOrReadOnly


from course.serializers import (
    CourseDetailSerializer, 
    CourseListSerializer,
    MaterialDetailSerializer,
    MaterialListSerializer,
    PictureSerializer,
    PictureCreateSerializer,
    HomeworkListSerializer,
    HomeworkDetailSerializer,
)

from django.http import FileResponse, Http404
from user_info.models import User, Student, Teacher
from rest_framework import generics

from course.utils import img_proccess_save

# Create your views here.

class CourseDetailView(APIView):
    """课程详情视图"""
    permission_classes = [IsTeacherOrReadOnly]

    @staticmethod
    def get_object(request, pk):
        try:
            course = Course.objects.get(pk=pk) # type: ignore
        except:
            raise Http404
        if request.user.is_student:
            try:
                course.students.all().get(pk=request.user.student.pk)
            except:
                return Response({"detail": "You have no right to access this course"}, status=status.HTTP_403_FORBIDDEN)
            return course
        if request.user.is_teacher:
            try:
                course.teachers.all().get(pk=request.user.teacher.pk)
            except:
                return Response({"detail": "You have no right to access this course"}, status=status.HTTP_403_FORBIDDEN)
            return course
        return Response({"detail": "You must be a student or a tracher to access this course"}, status=status.HTTP_403_FORBIDDEN)


    def get(self, request, pk):
        course = self.get_object(request, pk)
        if isinstance(course, Response):
            return course
        serializer = CourseDetailSerializer(course)
        return Response(serializer.data)


    def put(self, request, pk):
        course = self.get_object(request, pk)
        if isinstance(course, Response):
            return course
        serializer = CourseDetailSerializer(course, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        teachers = []
        if request.data.get('teachers') is not None and isinstance(request.data.get('teachers'), list):
            if len(request.data.get('teachers')) == 0:
                return Response({"teachers": "At least one teacher is required"}, status=status.HTTP_400_BAD_REQUEST)
            for id in request.data.get('teachers'):
                try:
                    user = User.objects.get(username=id)
                except:
                    return Response({"teachers": "id not found"}, status=status.HTTP_400_BAD_REQUEST)
                if not user.is_teacher:
                    return Response({"teachers": "only teachers can teach a course"}, status=status.HTTP_400_BAD_REQUEST)
                teachers.append(user.teacher)

        elif request.data.get('teachers') is not None:
            return Response({"teachers": "this field should be multi-valued"}, status=status.HTTP_400_BAD_REQUEST)

        students = []
        if request.data.get('students') is not None and isinstance(request.data.get('students'), list):
            for id in request.data.get('students'):
                try:
                    user = User.objects.get(username=id)
                except:
                    return Response({"students": "id not found"}, status=status.HTTP_400_BAD_REQUEST)
                if not user.is_student:
                    return Response({"students": "only students can take a course"}, status=status.HTTP_400_BAD_REQUEST)
                students.append(user.student)
        elif request.data.get('students') is not None:
            return Response({"students": "this field should be multi-valued"}, status=status.HTTP_400_BAD_REQUEST)

        prev_students = course.students.all()
        prev_teachers = course.teachers.all()
        if request.data.get('teachers') is None:
            if request.data.get('students') is None:
                serializer.save(students=prev_students, teachers=prev_teachers)
            else:
                serializer.save(students=students, teachers=prev_teachers)
        else:
            if request.data.get('students') is None:
                serializer.save(teachers=teachers, students=prev_students)
            else:
                serializer.save(students=students, teachers=teachers)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def delete(self, request, pk):
        course = self.get_object(request, pk)
        if isinstance(course, Response):
            return course
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseListView(APIView):
    """课程列表视图"""
    permission_classes = [IsTeacherOrReadOnly]
    lookup_field="id"
    def get(self, request):
        if request.user.is_student:
            try:
                courses = request.user.student.course_set.all()
            except:
                return Response({"detail": "No course taken"}, status=status.HTTP_404_NOT_FOUND)
            serializer = CourseListSerializer(courses, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.user.is_teacher:
            try:
                courses = request.user.teacher.course_set.all()
            except:
                return Response({"detail": "No course taught"},status=status.HTTP_404_NOT_FOUND)
            serializer = CourseListSerializer(courses, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "You must be a student or a teacher to access courses"}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        if request.user.is_teacher:
            serializer = CourseListSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save(teachers=[request.user.teacher], students=[])
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Only a teacher can create a course"}, status=status.HTTP_403_FORBIDDEN)


class MaterialDetailView(APIView):
    """课程资料详情视图"""
    permission_classes = [IsTeacherOrReadOnly]
    @staticmethod
    def get_object(request, pk1, pk):
        course = CourseDetailView.get_object(request, pk1)
        if isinstance(course, Response):
            return course
        try:
            material = course.materials.all().get(pk=pk)
        except:
            raise Http404
        if request.user.is_student and not material.is_public:
            return Response({"detail": "The material is not public now"}, status=status.HTTP_404_NOT_FOUND)
        return material

    def get(self, request, pk1, pk):
        material = self.get_object(request, pk1, pk)
        if isinstance(material, Response):
            return material
        serializer = MaterialDetailSerializer(material)
        if request.user.is_student:
            material.students.add(request.user.student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk1, pk):
        material = self.get_object(request, pk1, pk)
        if isinstance(material, Response):
            return material
        serializer = MaterialDetailSerializer(material, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk1, pk):
        material = self.get_object(request, pk1, pk)
        if isinstance(material, Response):
            return material
        material.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MaterialListView(APIView):
    """课程资料列表视图"""
    permission_classes = [IsTeacherOrReadOnly]
    lookup_field = "id"
    def get(self, request, pk1):
        course = CourseDetailView.get_object(request, pk1)
        if isinstance(course, Response):
            return course
        try:
            materials = course.materials.all()
            if request.user.is_student:
                materials = materials.filter(is_public=True)
        except:
            return Response({"detail": "No materials found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = MaterialListSerializer(materials, many=True, context={"request": request})
        datas = serializer.data
        new_datas = []
        for data in datas:
            i = data.get("id")
            data["url"] = request.build_absolute_uri() + str(i) + "/"
            new_datas.append(data)
        return Response(new_datas, status=status.HTTP_200_OK)

    def post(self, request, pk1):
        course = CourseDetailView.get_object(request, pk1)
        if isinstance(course, Response):
            return course
        serializer = MaterialListSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(teacher=request.user.teacher, course=course)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PictureListView(APIView):
    permission_classes = [IsTeacherOrReadOnly]
    lookup_field = "id"
    def get(self, request, pk1, pk2):
        material = MaterialDetailView.get_object(request, pk1, pk2)
        if isinstance(material, Response):
            return material
        try:
            pictures = material.pictures.all()
        except:
            return Response({"detail": "No pictures found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PictureSerializer(pictures, many=True, context={"request": request})
        datas = serializer.data
        new_datas = []
        for data in datas:
            i = data.get("id")
            data["url"] = request.build_absolute_uri() + str(i) + "/"
            new_datas.append(data)
        return Response(new_datas, status=status.HTTP_200_OK)

    def post(self, request, pk1, pk2):
        material = MaterialDetailView.get_object(request, pk1, pk2)
        if isinstance(material, Response):
            return material
        serializer = PictureCreateSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            image = serializer.validated_data.get("file_path")
            img_file = str(self.request.user.username)
            img_name, img_backend_relative_path = img_proccess_save(image, img_file)
            if serializer.validated_data.get("file_name") == "":
                serializer.save(material = material, file_path=img_backend_relative_path, file_name=img_name)
            else:
                serializer.save(material = material, file_path=img_backend_relative_path)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PictureDetailView(APIView):
    permission_classes = [IsTeacherOrReadOnly]
    lookup_field = "id"
    @staticmethod
    def get_object(request, pk1, pk2, pk):
        material = MaterialDetailView.get_object(request, pk1, pk2)
        if isinstance(material, Response):
            return material
        try:
            picture = material.pictures.all().get(pk=pk)
        except:
            raise Http404
        return picture

    def get(self, request, pk1, pk2, pk):
        picture = self.get_object(request, pk1, pk2, pk)
        if isinstance(picture, Response):
            return picture
        serializer = PictureSerializer(picture, context={"request":request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk1, pk2, pk):
        picture = self.get_object(request, pk1, pk2, pk)
        if isinstance(picture, Response):
            return picture
        if os.path.exists("." + picture.file_path.url):
            path = "." + picture.file_path.url
            os.remove(path)
            picture.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "path %s does not exist" % "." + picture.file_path.url}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def download_picture(request, pk1, pk2, pk):
    file_obj = PictureDetailView.get_object(request, pk1, pk2, pk)
    if isinstance(file_obj, Response):
        return file_obj
    return FileResponse(open(file_obj.file_path.path, 'rb'))



class HomeworkDetailView(APIView):
    permission_classes = [IsTeacherOrReadOnly]
    lookup_field = "id"
    @staticmethod
    def get_object(request, pk1, pk):
        course = CourseDetailView.get_object(request, pk1)
        if isinstance(course, Response):
            return course
        try:
            homework = course.homeworks.all().get(pk=pk)
        except:
            raise Http404
        if request.user.is_student:
            view_start_time = homework.view_start_time
            view_end_time = homework.view_end_time
            if timezone.now() > view_end_time:
                return Response({"detail": "The homework cannot be seen any more"}, status=status.HTTP_404_NOT_FOUND)
            elif timezone.now() < view_start_time:
                return Response({"detail": "The homework cannot be seen now"}, status=status.HTTP_404_NOT_FOUND)
        return homework

    def get(self, request, pk1, pk):
        homework = self.get_object(request, pk1, pk)
        if isinstance(homework, Response):
            return homework
        serializer = HomeworkDetailSerializer(homework, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk1, pk):
        homework = self.get_object(request, pk1, pk)
        if isinstance(homework, Response):
            return homework
        serializer = HomeworkDetailSerializer(homework, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk1, pk):
        homework = self.get_object(request, pk1, pk)
        if isinstance(homework, Response):
            return homework
        homework.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HomeworkListView(APIView):
    permission_classes = [IsTeacherOrReadOnly]
    lookup_field = "id"
    def get(self, request, pk1):
        course = CourseDetailView.get_object(request, pk1)
        if isinstance(course, Response):
            return course
        try:
            homeworks = course.homeworks.all()
        except:
            return Response({"detail": "No homeworks found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = HomeworkListSerializer(homeworks, many=True, context={"request": request})
        datas = serializer.data
        new_datas = []
        for data in datas:
            i = data.get("id")
            data["url"] = request.build_absolute_uri() + str(i) + "/"
            new_datas.append(data)
        return Response(new_datas, status=status.HTTP_200_OK)

    def post(self, request, pk1):
        course = CourseDetailView.get_object(request, pk1)
        if isinstance(course, Response):
            return course
        serializer = HomeworkListSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            serializer.save(course=course, teacher=request.user.teacher)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
