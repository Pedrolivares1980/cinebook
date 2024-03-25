from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone

# Import the views and serializers from the views.py and serializers.py files
from .models import Post, Comment
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
)
from .serializers import PostSerializer, CommentSerializer

# Get the custom user model
User = get_user_model()

class TestViews(TestCase):
    """
    Test the views in the app.
    """

    def setUp(self):
        """
        Create a user, a post, and a comment for testing.
        """
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user,
            date_posted=timezone.now()
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Test comment',
            date_posted=timezone.now()
        )

    def test_post_list_view(self):
        """
        Test the PostListView.
        """
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')
        self.assertContains(response, 'Test Post')

    def test_post_detail_view(self):
        """
        Test the PostDetailView.
        """
        response = self.client.get(reverse('post-detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertContains(response, 'Test Post')

    def test_post_create_view(self):
        """
        Test the PostCreateView.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            reverse('post-create'),
            {'title': 'New Test Post', 'content': 'New test content'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('post-detail', args=[2]))

    def test_post_update_view(self):
        """
        Test the PostUpdateView.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            reverse('post-update', args=[self.post.pk]),
            {'title': 'Updated Test Post', 'content': 'Updated test content'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('post-detail', args=[self.post.pk]))

    def test_post_delete_view(self):
        """
        Test the PostDeleteView.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('post-delete', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blog-home'))

    def test_comment_create_view(self):
        """
        Test the CommentCreateView.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            reverse('add-comment', args=[self.post.pk]),
            {'content': 'Test comment'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('post-detail', args=[self.post.pk]))

    def test_comment_update_view(self):
        """
        Test the CommentUpdateView.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            reverse('comment-update', args=[self.comment.pk]),
            {'content': 'Updated test comment'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('post-detail', args=[self.post.pk]))

    def test_comment_delete_view(self):
        """
        Test the CommentDeleteView.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('comment-delete', args=[self.comment.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('post-detail', args=[self.post.pk]))

    def test_post_create_view_invalid_input(self):
            """
            Test that a 200 error is returned when creating a post with no title or content.
            """
            self.client.login(username='testuser', password='testpassword')
            response = self.client.post(
                reverse('post-create'),
                {'title': '', 'content': ''}
            )
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'blog/post_form.html')
            self.assertContains(response, 'This field is required.')

    def test_post_detail_view_non_existent_post(self):
        """
        Test that a 404 error is returned when accessing a non-existent post.
        """
        response = self.client.get(reverse('post-detail', args=[999]))
        self.assertEqual(response.status_code, 404)

class TestSerializers(TestCase):
    """
    Test the serializers in the app.
    """

    def setUp(self):
        """
        Create a user, a post, and a comment for testing.
        """
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.post = Post.objects.create(
            title='Test Post',
            content='Testcontent',
            author=self.user,
            date_posted=timezone.now()
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Test comment',
            date_posted=timezone.now()
        )

    def test_post_serializer(self):
        """
        Test the PostSerializer.
        """
        serializer = PostSerializer(instance=self.post)
        self.assertEqual(serializer.data, {
            'id': int(self.post.pk),
            'title': 'Test Post',
            'content': 'Testcontent',
            'date_posted': self.post.date_posted.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'author': int(self.user.pk)
        })

    def test_comment_serializer(self):
        """
        Test the CommentSerializer.
        """
        serializer = CommentSerializer(instance=self.comment)
        self.assertEqual(serializer.data, {
            'id': int(self.comment.pk),
            'post': int(self.post.pk),
            'author': int(self.user.pk),
            'content': 'Test comment',
            'date_posted': self.comment.date_posted.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        })

        
# Test for model save methods
def test_post_save_method(self):
    """
    Test that the save method of the Post model is saving the correct data to the database.
    """
    post = Post(
        title='Test Post',
        content='Test content',
        author=self.user,
    )
    post.save()
    saved_post = Post.objects.get(pk=post.pk)
    self.assertEqual(saved_post.title, 'Test Post')
    self.assertEqual(saved_post.content, 'Test content')
    self.assertEqual(saved_post.author, self.user)