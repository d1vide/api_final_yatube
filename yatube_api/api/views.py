from rest_framework import viewsets
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework import filters
from .serializers import (GroupSerializer,
                          PostSerializer,
                          CommentSerializer,
                          FollowSerializer)
from .permissions import AuthorOrSafeMethodsOnly

from posts.models import Group, Post, Comment, Follow, User


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorOrSafeMethodsOnly, IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrSafeMethodsOnly, IsAuthenticatedOrReadOnly,)

    def get_post_object(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        return Comment.objects.filter(post=self.get_post_object())

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post_object())


class ListCreateViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    pass


class FollowViewSet(ListCreateViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('following__username',)

    def get_user(self):
        return get_object_or_404(User,
                                 username=self.request.data.get('following'))

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user, following=self.get_user())
        return super().perform_create(serializer)

    def get_queryset(self):
        return self.request.user.follow.all()
