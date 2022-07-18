from email.mime import image
from rest_framework import serializers

from .models import Post

class PostSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    image = serializers.ImageField(max_length=None, allow_empty_file=True,allow_null=True,required=False)

    class Meta:
        model = Post
        fields = "__all__"

    def get_image(self, post):
        request = self.context.get('request')
        if post.image:
            image_url = post.image.url
            return request.build_absolute_uri(image_url)
        return ''

class PostListViewSerializer(serializers.ModelSerializer):

    author = serializers.CharField(source='author.username', read_only=True)
    likes = serializers.SerializerMethodField()
    loves = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "author", "body", "likes", "loves", "views", "created_at", "image"]

    def get_image(self, post):
        request = self.context.get('request')
        if post.image:
            image_url = post.image.url
            return request.build_absolute_uri(image_url)
        return ''

    def get_likes(self, post):
        return post.likes.count()

    def get_loves(self, post):
        return post.loves.count()