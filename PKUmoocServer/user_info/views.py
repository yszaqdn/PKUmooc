from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from user_info.models import User, Dept
from user_info.models import Student
from user_info.models import Teacher


from user_info.serializers import (
    UserSerializer,
    UserRegisterSerializer,
    StudentRegisterSerializer,
    StudentSerializer,
    DeptSerializer,
    TeacherRegisterSerializer,
    TeacherSerializer,
)

from rest_framework.permissions import (
    AllowAny, 
    IsAuthenticatedOrReadOnly, 
    IsAdminUser,
)
from user_info.permissions import (
    IsAdminUserOrReadOnly, 
    IsAdminUserOrNotRegistered,
    IsAdminUserOrSelf,
)

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUserOrSelf]

        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserRegisterSerializer
        else:
            return UserSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        else:
            return [User.objects.get(id=self.request.user.id)]

    def get_object(self):
        return User.objects.get(user=self.request.user)


class DeptViewSet(viewsets.ModelViewSet):
    queryset = Dept.objects.all()
    serializer_class = DeptSerializer
    lookup_field = 'name'
    permission_classes = [IsAdminUserOrReadOnly]


class StudentViewSet(viewsets.ModelViewSet):
    lookup_field = 'user'
    permission_classes = [IsAdminUserOrNotRegistered]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return StudentRegisterSerializer
        else:
            return StudentSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Student.objects.all()
        else:
            return [Student.objects.get(user=self.request.user)]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_object(self):
        return Student.objects.get(user=self.request.user)


class TeacherViewSet(viewsets.ModelViewSet):
    lookup_field = 'user'
    permission_classes = [IsAdminUserOrNotRegistered]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TeacherRegisterSerializer
        else:
            return TeacherSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Teacher.objects.all()
        else:
            return [Teacher.objects.get(user=self.request.user)]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_object(self):
        return Teacher.objects.get(user=self.request.user)
