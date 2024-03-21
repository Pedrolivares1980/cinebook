from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.
    """
    class Meta:
        """
        Meta class for the PostSerializer.
        """
        model = Post
        fields = ['id', 'title', 'content', 'date_posted', 'author']

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    """
    class Meta:
        """
        Meta class for the CommentSerializer.
        """
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'date_posted']