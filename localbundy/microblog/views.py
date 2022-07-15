from django.shortcuts import render
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from authentication.models import User
from .serializers import PostSerializer, PostListViewSerializer
from .models import Post
from .pagination import PostListPagination

class CreateBlogPostAPI(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = User.objects.get(email = request.user)
        data = request.data.copy()
        data['author'] = user.id
        serializer = PostSerializer(data=data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            id = serializer.data.get('id')
            post = Post.objects.get(id=id)
            view_serializer = PostListViewSerializer(post, context={'request':request})
            return Response(view_serializer.data)
        return Response(serializer.errors)

class BlogPostDetailAPI(APIView):
    '''
    Gets the post details and adds views on every request
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            blogpost = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({"success":False, "message": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND)
        blogpost.views = blogpost.views + 1
        blogpost.save()
        serializer = PostListViewSerializer(blogpost, context={'request':request})
        return Response({"success":True, "data":serializer.data})

class LikeAPI(APIView):
    '''
    The accepts a Post ID and likes and unlikes the Post
    '''

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        user = User.objects.get(email = request.user)
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({"success":False, "message":"Post doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        is_liked = post.likes.filter(id = user.id)

        if is_liked:
            post.likes.remove(user.id)
            message = "Post unliked!"
        else:
            post.likes.add(user.id)
            message = "Post liked!"
        post.save()

        serializer = PostListViewSerializer(post, context={'request':request})
        return Response({"success": True, "message":message, "data":serializer.data})

class LoveAPI(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        user = User.objects.get(email = request.user)
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({"success":False, "message":"Post doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        is_loved = post.loves.filter(id = user.id)

        if is_loved:
            post.loves.remove(user.id)
            message = "Love removed!"
        else:
            post.loves.add(user.id)
            message = "Love added"
        post.save()

        serializer = PostListViewSerializer(post, context={'request':request})
        return Response({"success": True, "message":message, "data":serializer.data})

class AddPostViewAPI(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        user = User.objects.get(email = request.user)
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({"success":False, "message":"Post doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        print("request.session.session_key",request.session.session_key)
        print("request.META['REMOTE_ADDR']", request.META['REMOTE_ADDR'])
        # is_liked = post.views.filter(id = user.id)

        # if is_liked:
        #     post.loves.remove(user.id)
        #     message = "Love added!"
        # else:
        #     post.loves.add(user.id)
        #     message = "Love removed"
        # post.save()

        # serializer = PostSerializer(post, context={'request':request})
        # return Response({"success": True, "message":message, "data":serializer.data})
        return Response()

class BlogPostList(ListAPIView):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostListViewSerializer
    pagination_class = PostListPagination