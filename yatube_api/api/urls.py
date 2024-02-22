from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import GroupViewSet, PostViewSet, CommentViewSet, FollowViewSet

router_v1 = DefaultRouter()
router_v1.register(r'groups', GroupViewSet)
router_v1.register(r'posts', PostViewSet)
router_v1.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet)
router_v1.register(r'follow', FollowViewSet)


urlpatterns = [
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router_v1.urls)),

]
