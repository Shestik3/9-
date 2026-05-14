"""Serializers for the API application."""

from rest_framework import serializers
from posts.models import Post, Group, Comment


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model."""

    author = serializers.SerializerMethodField()

    class Meta:
        """Meta options for PostSerializer."""

        model = Post
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
            'image',
            'group',
        )
        read_only_fields = ('author',)

    def get_author(self, obj):
        """Return author username as string."""
        return obj.author.username


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for Group model."""

    class Meta:
        """Meta options for GroupSerializer."""

        model = Group
        fields = (
            'id',
            'title',
            'slug',
            'description',
        )


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model."""

    author = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()

    class Meta:
        """Meta options for CommentSerializer."""

        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'post',
            'created',
        )
        read_only_fields = ('author', 'post')

    def get_author(self, obj):
        """Return author username as string."""
        return obj.author.username

    def get_post(self, obj):
        """Return post id as integer."""
        return obj.post.id
