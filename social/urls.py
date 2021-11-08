from django.urls import path
from .views import (
    AddBodyView,
    PostDeleteView,
    PostDetailView,
    CommentEditView,
    CommentDeleteView,
    CommentReplyView,
    CommentFather,
    CategorySearch,
    EditPost,
    TagSearch,
    HomeBlogView,
    EditBodyPostView,
    BodyPostDeleteView
)
app_name = "social"
urlpatterns = [
    path('blog/',HomeBlogView.as_view(),name="blog"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="post-detail"),
    path('post/edit/<int:pk>', EditPost, name="post-edit"),

    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name="post-delete"),
    path('post/<int:post_pk>/comment/delete/<int:pk>/',
         CommentDeleteView.as_view(), name="comment-delete"),
    
    
    path('post/<int:post_pk>/body/delete/<int:pk>/',
         BodyPostDeleteView.as_view(), name="body-delete"),
    
    
    path('post/<int:post_pk>/comment/edit/<int:pk>/',
         CommentEditView.as_view(), name="comment-edit"),
    
    path('post/<int:post_pk>/body/edit/<int:pk>/',
         EditBodyPostView.as_view(), name="body-edit"),
    

    path('post/<int:post_pk>/comment/<int:pk>/reply',
         CommentReplyView.as_view(), name='comment-reply'),

    path('post/<int:pk>/father',
         CommentFather.as_view(), name='comment-father'),
    path('post/search', CategorySearch.as_view(), name='category-search'),
    path('post/search/tag/', TagSearch.as_view(), name='tag-search'),



]
