from django.urls import path

from .views import *

urlpatterns = [
    path("create/", CreateBlogPostAPI.as_view(), name='create_post'),
    path("get/<int:pk>/", BlogPostDetailAPI.as_view(), name='get_post'),
    path("list/", BlogPostList.as_view(), name='post_list'),
    path("like/<int:pk>/", LikeAPI.as_view(), name='post_like'),
    path("love/<int:pk>/", LoveAPI.as_view(), name='post_love'),
    path("view/<int:pk>/", AddPostViewAPI.as_view(), name='add_post_view'),

]
