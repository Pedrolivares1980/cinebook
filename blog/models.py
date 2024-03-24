from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

# Abstract base class for Like functionality
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

# Model for blog posts
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # ManyToManyField to represent likes for the post. 'through' specifies the custom through model.
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_likes', through='PostLike')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

    # Method to count the number of likes
    def total_likes(self):
        return self.likes.count()

# Model for comments on blog posts
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    # ManyToManyField to represent likes for the comment. 'through' specifies the custom through model.
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_likes', through='CommentLike')

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.post.pk})

    # Method to count the number of likes
    def total_likes(self):
        return self.likes.count()

# Through model for post likes, linking the Like model to the Post model
class PostLike(Like):
    post = models.ForeignKey(Post, related_name='likes_details', on_delete=models.CASCADE)

# Through model for comment likes, linking the Like model to the Comment model
class CommentLike(Like):
    comment = models.ForeignKey(Comment, related_name='likes_details', on_delete=models.CASCADE)