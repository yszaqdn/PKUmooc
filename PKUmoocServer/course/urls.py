from django.urls import path
from course import views

app_name="course"
urlpatterns = [
    path("", views.CourseListView.as_view(), name="course-list"),
    path("<str:pk>/", views.CourseDetailView.as_view(), name="course-detail"),
    path("<str:pk1>/material/", views.MaterialListView.as_view(), name="material-list"),
    path("<str:pk1>/material/<int:pk>/", views.MaterialDetailView.as_view(), name="material-detail"),
    path("<str:pk1>/material/<int:pk2>/picture/", views.PictureListView.as_view(), name="picture-list"),
    path("<str:pk1>/material/<int:pk2>/picture/<str:pk>/", views.PictureDetailView.as_view(), name="picture-detail"),
    path("<str:pk1>/material/<int:pk2>/picture/<str:pk>/download/", views.download_picture, name="picture-download"),
    path("<str:pk1>/homework/", views.HomeworkListView.as_view(), name="homework-list"),
    path("<str:pk1>/homework/<int:pk>/", views.HomeworkDetailView.as_view(), name="homework-detail"),
]
