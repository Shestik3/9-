from rest_framework import routers
from .views import PostViewSet, GroupViewSet, CommentViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('groups', GroupViewSet, basename='groups')

# Комментарии — вложенный ресурс
comment_patterns = [
    path(
        '',
        CommentViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='comments-list'
    ),
    path(
        '<int:pk>/',
        CommentViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='comments-detail'
    ),
]

urlpatterns = [
    path('', include(router.urls)),
    path(
        'posts/<int:post_id>/comments/',
        include((comment_patterns, 'comments'), namespace='comments')
    ),
]
