"""
URL configuration for PKUmoocServer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from user_info import views
from PKUmoocServer import settings
from django.views.static import serve

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
#
# router = DefaultRouter()
# router.register(r'user', views.UserViewSet)
# router.register(r'dept', views.DeptViewSet)
# router.register(r'student', views.StudentViewSet, basename="student")
# router.register(r'teacher', views.TeacherViewSet, basename="teacher")
#
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    # path("api/", include(router.urls)),
    path("api/token/", views.TokenObtainPairView.as_view(), name="token_obtain_pairi"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/register/", views.user_register, name="register"),
    # path("api/student/", views.student_register, name="register")
    path("api/course/", include("course.urls"), name="course"),
    re_path(r"media/(?P<path>.*)$", serve, {"document_root":settings.MEDIA_ROOT}),
]
