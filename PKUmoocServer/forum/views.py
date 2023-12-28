from django.shortcuts import render

# Create your views here.


from rest_framework import viewsets

from forum.models import Forum, ForumSection, Post, Reply
from forum.serializers import ForumSerializer, ForumSectionSerializer, PostSerializer, ReplySerializer
from forum.permissions import IsReadOnly, IsTeacherOrReadOnly,IsTeacherOrOwner

class ForumViewSet(viewsets.ModelViewSet):
    # 讨论区
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    permission_classes = [IsReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ForumSectionViewSet(viewsets.ModelViewSet):
    queryset = ForumSection.objects.all()
    serializer_class = ForumSectionSerializer
    permission_classes = [IsTeacherOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsTeacherOrOwner]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [IsTeacherOrOwner]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)