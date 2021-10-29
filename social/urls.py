from django.urls import path
from .views import (
    AddBodyView,
    PostDeleteView,
    PostDetailView,
    PostEditView,
    CommentEditView,
    CommentDeleteView,
    CommentReplyView,
    UserSearch
)
app_name = "social"
urlpatterns = [
    path('post/<int:pk>/', PostDetailView.as_view(), name="post-detail"),
    path('post/edit/<int:pk>/', PostEditView.as_view(), name="post-edit"),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name="post-delete"),
#     path('post/<int:pk>/', AddBodyView.as_view(), name="body-detail"),
    
    path('post/<int:post_pk>/comment/delete/<int:pk>/',
         CommentDeleteView.as_view(), name="comment-delete"),
    path('post/<int:post_pk>/comment/edit/<int:pk>/',
         CommentEditView.as_view(), name="comment-edit"),

    path('post/<int:post_pk>/comment/<int:pk>/reply',
         CommentReplyView.as_view(), name='comment-reply'),

    path('seach/', UserSearch.as_view(), name='profile-search'),



]
