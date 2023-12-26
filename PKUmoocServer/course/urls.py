from django.urls import path
from course import views

app_name="course"
urlpatterns = [
    path("", views.CourseListView.as_view(), name="course-list"),
    path("<str:pk>/", views.CourseDetailView.as_view(), name="course-detail"),
    path("<str:pk1>/material/", views.MaterialListView.as_view(), name="material-list"),
    path("<str:pk1>/material/<int:pk>/", views.MaterialDetailView.as_view(), name="material-detail"),
]
