from django.shortcuts import render
from django.http import HttpResponse
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

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

class ForumSectionViewSet(viewsets.ModelViewSet):
    queryset = ForumSection.objects.all()
    serializer_class = ForumSectionSerializer
    permission_classes = [IsTeacherOrReadOnly]

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsTeacherOrOwner]

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [IsTeacherOrOwner]

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)


def forum(request, forum_name):
    return HttpResponse("You're looking at the forum %s." % forum_name)


def forumsection(request, forumsection_id):
    response = "You're looking at the forumsection %s." 
    return HttpResponse(response % forumsection_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)