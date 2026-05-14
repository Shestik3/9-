from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from posts.models import Post, Group, Comment
from .serializers import (
    PostSerializer,
    GroupSerializer,
    CommentSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для постов (полный CRUD)"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def perform_create(self, serializer):
        """При создании поста устанавливаем автора"""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Проверка прав на редактирование"""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied(
                'Изменение чужого контента запрещено!'
            )
        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        """Проверка прав на удаление"""
        if instance.author != self.request.user:
            raise PermissionDenied(
                'Удаление чужого контента запрещено!'
            )
        return super().perform_destroy(instance)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для групп (только чтение)"""
    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев (полный CRUD)"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        """Получаем комментарии конкретного поста"""
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(
            post_id=post_id
        ).order_by('id')

    def perform_create(self, serializer):
        """При создании комментария устанавливаем автора и пост"""
        post_id = self.kwargs.get('post_id')
        serializer.save(
            author=self.request.user,
            post_id=post_id
        )

    def perform_update(self, serializer):
        """Проверка прав на редактирование"""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied(
                'Изменение чужого контента запрещено!'
            )
        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        """Проверка прав на удаление"""
        if instance.author != self.request.user:
            raise PermissionDenied(
                'Удаление чужого контента запрещено!'
            )
        return super().perform_destroy(instance)
