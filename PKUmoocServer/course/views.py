from rest_framework.response import Response
from rest_framework.schemas.coreapi import serializers
from course.models import Course
from rest_framework.views import APIView, status

from course.serializers import CourseDetailSerializer, CourseListSerializer

from django.http import Http404
from user_info.models import User, Student, Teacher
from rest_framework import generics

# Create your views here.

class CourseDetailView(APIView):
    """课程详情视图"""

    def get_object(self, request, pk):
        try:
            course = Course.objects.get(pk=pk) # type: ignore
        except:
            raise Http404
        if request.user.is_student:
            try:
                course.students.all().get(pk=request.user.student.pk)
            except:
                return Response({"error": "You have no right to access this course"}, status=status.HTTP_403_FORBIDDEN)
            return course
        if request.user.is_teacher:
            try:
                course.teachers.all().get(pk=request.user.teacher.pk)
            except:
                return Response({"error": "You have no right to access this course"}, status=status.HTTP_403_FORBIDDEN)
            return course
        return Response({"error": "You must be a student or a tracher to access this course"}, status=status.HTTP_403_FORBIDDEN)


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
        return Response(serializer.data)


    def delete(self, request, pk):
        course = self.get_object(request, pk)
        if isinstance(course, Response):
            return course
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseListView(APIView):
    lookup_field="id"
    """课程列表视图"""
    def get(self, request):
        if request.user.is_student:
            try:
                courses = request.user.student.course_set.all()
            except:
                return Response({"error": "No course taken"}, status=status.HTTP_404_NOT_FOUND)
            serializer = CourseListSerializer(courses, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.user.is_teacher:
            try:
                courses = request.user.teacher.course_set.all()
            except:
                return Response({"error": "No course taught"},status=status.HTTP_404_NOT_FOUND)
            serializer = CourseListSerializer(courses, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "You must be a student or a teacher to access courses"}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        if request.user.is_teacher:
            serializer = CourseListSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save(teachers=[request.user.teacher], students=[])
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Only a teacher can create a course"}, status=status.HTTP_403_FORBIDDEN)
