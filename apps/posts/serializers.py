from rest_framework import serializers 

from apps.auth.models import User
from apps.auth.serializers import UserShortSerializer

from .models import Post, Comment, Like

# вспомогательные serializers
class CommentListSerializer(serializers.ModelSerializer):
    author = UserShortSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at']


class LikeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ['user']


# post serializers
class PostListSerializer(serializers.ModelSerializer):
    author = UserShortSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at']


class PostGetSerializer(serializers.ModelSerializer):
    author = UserShortSerializer(read_only=True)
    comments = CommentListSerializer(many=True, read_only=True)
    likes = LikeListSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 
            'author', 
            'title', 
            'content', 
            'created_at', 
            'comments', 
            'likes',
            'likes_count'
        ]


class PostCreateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=5, max_length=255)
    content = serializers.CharField(max_length=10000)


class PostUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(
        min_length=5, 
        max_length=255, 
    )
    content = serializers.CharField(
        max_length=10000, 
    )


class CommentCreateSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=2000)



# feed serializers
class PostFeedSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'likes', 'likes_count']
    
    def get_likes(self, obj):
        return [like.user_id for like in obj.likes.all()]

    def get_likes_count(self, obj):
        return len(obj.likes.all())
    

class UserFeedSerializer(serializers.ModelSerializer):
    posts = PostFeedSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'full_name', 'posts']