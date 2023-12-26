from django.urls import path
from course.views import CourseDetailView, CourseListView

app_name="course"
urlpatterns = [
    path("", CourseListView.as_view(), name="course-list"),
    path("<str:pk>/", CourseDetailView.as_view(), name="course-detail"),
]
