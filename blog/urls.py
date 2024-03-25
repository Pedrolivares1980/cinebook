from django.urls import path
from . import views


urlpatterns = [
    path("", views.PostListView.as_view(), name="blog-home" ),
    path('about/', views.about, name='blog-about'),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("post/new/", views.PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post-update"), 
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"), 
    path("post/<int:pk>/comment/", views.CommentCreateView.as_view(), name="add-comment"),
    path("comment/<int:pk>/update/", views.CommentUpdateView.as_view(), name="comment-update"),
    path("comment/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment-delete"),
    path("like/<int:pk>/", views.likeView, name="like_post"),
    path("comment_like/<int:pk>/", views.commentLikeView, name="comment_like_post"),
]