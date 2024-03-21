from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

class Post(models.Model):
    """
    Represents a blog post created by a user.
    """
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        """
        Return the title of the post as its string representation.
        """
        return self.title

    def get_absolute_url(self):
        """
        Return the URL to access the detail view of this post.
        """
        return reverse("post-detail", kwargs={"pk": self.pk})

class Comment(models.Model):
    """
    Represents a comment made on a blog post.
    """
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )

    def is_author(self, user):
        """
        Check if the provided user is the author of the comment.
        """
        return self.author == user

    def __str__(self):
        """
        Return a string representation of the comment.
        """
        return f"Comment by {self.author.username} on {self.post.title}"

    def get_absolute_url(self):
        """
        Return the URL to access the detail view of the post associated with this comment.
        """
        return reverse("post-detail", kwargs={"pk": self.post.pk})