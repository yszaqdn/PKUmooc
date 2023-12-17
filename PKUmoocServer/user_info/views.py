from django.shortcuts import render

from rest_framework import viewsets

from user_info.models import User
from user_info.models import Student
from user_info.models import Teacher

from user_info.serializers import UserSerializer
from user_info.serializers import StudentSerializer
from user_info.serializers import TeacherSerializer

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
