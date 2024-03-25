from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
    """Model representing a blog post."""

    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='blog_posts')

    def total_likes(self):
        """Return the total number of likes for this post."""
        return self.likes.count()
    
    def __str__(self):
        """String representation of the Post."""
        return self.title 

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this Post."""
        return reverse("post-detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    """Model representing a comment on a blog post."""

    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_likes')
    
    def is_author(self, user):
        """
        Determine if the given user is the author of this comment.
        """
        return self.author == user
    
    def total_comment_likes(self):
        """
        Return the total number of likes on this comment.
        """
        return self.likes.count()

    def __str__(self):
        """String representation of the Comment."""
        return f"Comment by {self.author.username} on {self.post.title}"

    def get_absolute_url(self):
        """Returns the URL to access a detail record for the Post associated with this Comment."""
        return reverse("post-detail", kwargs={"pk": self.post.pk})