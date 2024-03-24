from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    CommentCreateView,
    CommentReplyView,
    CommentUpdateView,
    CommentDeleteView,
)

# Define the URL patterns for the blog app
urlpatterns = [
    # Home page URL pattern
    path('', PostListView.as_view(), name='blog-home'),

    # About page URL pattern
    path('about/', views.about, name='blog-about'),

    # Post detail page URL pattern
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),

    # Post create page URL pattern
    path('post/new/', PostCreateView.as_view(), name='post-create'),

    # Post update page URL pattern
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),

    # Post delete page URL pattern
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    # User post list page URL pattern
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),

    # Comment create page URL pattern
    path("post/<int:pk>/comment/", CommentCreateView.as_view(), name="add-comment"),

    # Comment reply page URL pattern
    path("post/<int:post_id>/comment/<int:parent_id>/reply/", CommentReplyView.as_view(), name="add-reply"),

    # Comment update page URL pattern
    path("comment/<int:pk>/update/", CommentUpdateView.as_view(), name="comment-update"),

    # Comment delete page URL pattern
    path("comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),
    
    path('like_post/', views.like_post, name='like_post'),
    path('like_comment/', views.like_comment, name='like_comment'),

]