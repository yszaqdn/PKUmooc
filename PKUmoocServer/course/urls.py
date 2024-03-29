from django.urls import path, include
from course import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"post", views.PostViewSet)

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
    path("<str:pk1>/homework/<int:pk2>/problem/", views.ProblemListView.as_view(), name="problem-list"),
    path("<str:pk1>/homework/<int:pk2>/problem/<int:pk>/", views.ProblemDetailView.as_view(), name="problem-detail"),
    path("<str:pk1>/homework/<int:pk2>/submission/", views.SubmissionListView.as_view(), name="submission-list"),
    path("<str:pk1>/homework/<int:pk2>/submission/<int:pk>/", views.SubmissionDetailView.as_view(), name="submission-detail"),
    path("<str:pk1>/student/", views.StudentListView.as_view(), name="student-list"),
    path("<str:pk1>/student/<int:pk>/", views.StudentDetailView.as_view(), name="student-detail"),
    path("<str:pk1>/section/", views.ForumSectionListView.as_view(), name="section-list"),
    path("<str:pk1>/", include(router.urls)),
]
