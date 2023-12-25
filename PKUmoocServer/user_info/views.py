from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from user_info.models import User
from user_info.models import Student
from user_info.models import Teacher

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from user_info.serializers import (
    RegisterSerializer,
    UserSerializer,
    UserRegisterSerializer,
    StudentRegisterSerializer,
    StudentSerializer,
    
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

from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.request import Request

# Create your views here.

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     lookup_field = 'username'
#
#     def get_permissions(self):
#         if self.request.method == 'POST':
#             self.permission_classes = [AllowAny]
#         else:
#             self.permission_classes = [IsAdminUserOrSelf]
#
#         return super().get_permissions()
#
#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return UserRegisterSerializer
#         else:
#             return UserSerializer
#
#     def get_queryset(self):
#         if self.request.user.is_superuser:
#             return User.objects.all()
#         else:
#             return [User.objects.get(id=self.request.user.id)]
#
#     def get_object(self):
#         return User.objects.get(user=self.request.user)
#




# class StudentViewSet(viewsets.ModelViewSet):
#     lookup_field = 'user'
#     permission_classes = [IsAdminUserOrNotRegistered]
#
#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return StudentRegisterSerializer
#         else:
#             return StudentSerializer
#
#     def get_queryset(self):
#         if self.request.user.is_superuser:
#             return Student.objects.all()
#         else:
#             return [Student.objects.get(user=self.request.user)]
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#     def get_object(self):
#         return Student.objects.get(user=self.request.user)
#
#
# class TeacherViewSet(viewsets.ModelViewSet):
#     lookup_field = 'user'
#     permission_classes = [IsAdminUserOrNotRegistered]
#
#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return TeacherRegisterSerializer
#         else:
#             return TeacherSerializer
#
#     def get_queryset(self):
#         if self.request.user.is_superuser:
#             return Teacher.objects.all()
#         else:
#             return [Teacher.objects.get(user=self.request.user)]
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#     def get_object(self):
#         return Teacher.objects.get(user=self.request.user)
#
class TokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """

    _serializer_class = api_settings.TOKEN_OBTAIN_SERIALIZER

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        try:
            user = User.objects.get(username=request.data.get("username"))
        except:
            pass

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        user = User.objects.get(id=user.id)
        data = {}
        data["refresh"] = serializer.validated_data.get("refresh")
        data["access"]  = serializer.validated_data.get("access")
        data["is_student"] = user.is_student
        data["is_teacher"] = user.is_teacher
        return Response(data, status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
def user_register(request):
    if request.method == "GET":
        try:
            if request.user.is_teacher:
                return Response({'identity': 'teacher'}, status=status.HTTP_200_OK)
            elif request.user.is_student:
                return Response({'identity': 'student'}, status=status.HTTP_200_OK)
            else:
                return Response({'identity': 'other'}, status=status.HTTP_200_OK)
        except AttributeError:
            return Response({'identity': 'login required'}, status=status.HTTP_401_UNAUTHORIZED)

    # read the request
    args_serializer = RegisterSerializer(data=request.data)
    if args_serializer.is_valid():
        data = args_serializer.data

        # Conform the password
        if data.get('password') != data.pop('confirmpassword'):
            return Response({'error': 'Improper password'}, status=status.HTTP_400_BAD_REQUEST)

        # Create user
        username = data.get('id')
        data['username'] = username
        user_serializer = UserRegisterSerializer(data=data)
        if user_serializer.is_valid():
            user_serializer.save()
            user = User.objects.get(username=username)
            data.pop('username')
            data.pop('password')

            # Register student
            if data.get('identity') == 'student':
                student_serializer = StudentRegisterSerializer(data=data)
                if student_serializer.is_valid():
                    student_serializer.save(user=user)
                    return Response(data, status=status.HTTP_201_CREATED)
                user.delete()
                return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Register teacher
            elif data.get('identity') == 'teacher':
                teacher_serializer = TeacherRegisterSerializer(data=data)
                if teacher_serializer.is_valid():
                    teacher_serializer.save(user=user)
                    return Response(data, status=status.HTTP_201_CREATED)
                user.delete()
                return Response(teacher_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Handle errors
            else:
                user.delete()
                return Response({'identity': 'must be a student or a teacher'}, status=status.HTTP_400_BAD_REQUEST)
        elif user_serializer.errors.get('username') is not None:
            errs = user_serializer.errors.pop('username')
            if "A user with that username already exists." in errs:
                return Response({"id":["A user with that id already exists."]}, status=status.HTTP_400_BAD_REQUEST)
    return Response(args_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
