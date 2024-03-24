from venv import logger
from django import forms
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Comment, PostLike, CommentLike
from django.http import JsonResponse
import json

class PostListView(ListView):
    """
    View to display a list of all blog posts.
    """
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        """
        Add the main comments to the context data.
        """
        context = super().get_context_data(**kwargs)
        context['posts_with_comments_count'] = [
            {
                'post': post,
                'comments_count': Comment.objects.filter(post=post).count()            }
            for post in context['posts']
        ]
        return context


class PostDetailView(DetailView):
    """
    View to display the details of a specific blog post, including its main comments.
    """
    model = Post

    def get_context_data(self, **kwargs):
        """
        Add the main comments to the context data.
        """
        context = super().get_context_data(**kwargs)
        context["main_comments"] = Comment.objects.filter(
            post=self.get_object(), parent__isnull=True
        ).order_by("-date_posted")
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    """
    View to create a new blog post.
    """
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        """
        Set the author of the post to the logged in user.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View to update an existing blog post.
    """
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        """
        Set the author of the post to the logged in user.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        """
        Ensure only the author of the post can update it.
        """
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View to delete an existing blog post.
    """
    model = Post
    success_url = '/blog/'

    def test_func(self):
        """
        Ensure only the author of the post can delete it.
        """
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class UserPostListView(ListView):
    """
    View to display a list of all blog posts by a specific user.
    """
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        """
        Return the blog posts for the user.
        """
        self.user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=self.user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        """
        Add the main comments to the context data.
        """
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(author=self.user)
        return context
    
class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    View to create a new comment on a blog post.
    """
    model = Comment
    fields = ["content"]
    template_name = "blog/add_comment.html"

    def get_form(self, form_class=None):
        """
        Set the widget and label attributes for the content field.
        """
        form = super().get_form(form_class)
        form.fields['content'].widget = forms.Textarea(attrs={
            'rows': 8,
            'style': 'resize:none;',  
            'placeholder': 'Write your comment here...'
        })
        form.fields['content'].label = ''
        return form

    def form_valid(self, form):
        """
        Set the author of the comment to the logged in user.
        """
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        """
        Redirect to the detail view of the post associated with the comment.
        """
        return reverse_lazy("post-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        """
        Add the main comments to the context data.
        """
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        context['post_detail'] = {
            'author_profile_image': post.author.profile.image.url,
            'author_username': post.author.username,
            'date_posted': post.date_posted,
            'title': post.title,
            'content': post.content
        }
        return context


class CommentReplyView(LoginRequiredMixin, CreateView):
    """
    View to create a reply to a comment.
    """
    model = Comment
    fields = ["content"]
    template_name = "blog/add_reply.html"

    def get_form(self, form_class=None):
        """
        Set the widget and label attributes for the content field.
        """
        form = super().get_form(form_class)
        form.fields['content'].widget = forms.Textarea(attrs={
            'rows': 8,
            'style': 'resize:none;',  
            'placeholder': 'Write your comment here...'
        })
        form.fields['content'].label = ''
        return form

    def form_valid(self, form):
        """
        Set the author, parent, and post of the reply.
        """
        form.instance.author = self.request.user
        form.instance.parent_id = self.kwargs["parent_id"]
        form.instance.post_id = self.kwargs["post_id"]
        return super().form_valid(form)

    def get_success_url(self):
        """
        Redirect to the detail view of the post associated with the comment.
        """
        return reverse_lazy("post-detail", kwargs={"pk": self.kwargs["post_id"]})

    def get_context_data(self, **kwargs):
        """
        Add the parent comment to the context data.
        """
        context = super().get_context_data(**kwargs)
        parent_comment = get_object_or_404(Comment, pk=self.kwargs['parent_id'])
        context['parent_comment'] = parent_comment
        return context


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View to update an existing comment.
    """
    model = Comment
    fields = ["content"]
    template_name = "blog/comment_update.html"

    def form_valid(self, form):
        """
        Set the author of the comment to the logged in user.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """
        Ensure only the author of the comment can update it.
        """
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        """
        Redirect to the detail view of the post associated with the comment.
        """
        return reverse_lazy("post-detail", kwargs={"pk": self.object.post.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View to delete an existing comment.
    """
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def test_func(self):
        """
        Ensure only the comment author can delete the comment.
        """
        comment = self.get_object()
        if self.request.user != comment.author:
            raise PermissionDenied("You are not allowed to delete this comment.")
        return True

    def get_success_url(self):
        """
        Redirect to the associated post's detail page after deletion.
        """
        return reverse_lazy("post-detail", kwargs={"pk": self.object.post.pk})

    def form_valid(self, form):
        """
        Overridden to handle recursive deletion of comments.
        """
        comment = self.get_object()
        try:
            self._recursive_delete(comment)
        except Exception as e:
            logger.error(f"Error occurred while deleting comment {comment.id}: {e}", exc_info=True)

        return super().form_valid(form)

    def _recursive_delete(self, comment):
        """
        Recursively delete child comments before deleting the comment itself.
        """
        for child_comment in comment.replies.all():
            self._recursive_delete(child_comment)
        comment.delete()

@require_POST
@login_required
def like_post(request):
    # Parse the JSON body of the request
    data = json.loads(request.body)
    post_id = data.get('id')

    # Fetch the post by ID
    post = Post.objects.get(id=post_id)
    liked = False  # Default to not liked

    if post.likes.filter(id=request.user.id).exists():
        # If the user already liked this post, unlike it
        post.likes.remove(request.user)
    else:
        # Otherwise, like it
        post.likes.add(request.user)
        liked = True

    return JsonResponse({'total_likes': post.likes.count(), 'liked': liked})

def like_comment(request):
    comment_id = request.POST.get('id')
    comment = Comment.objects.get(id=comment_id)
    
    if comment.liked_by_user(request.user):
        comment.likes.filter(user=request.user).delete()
        liked = False
    else:
        CommentLike.objects.create(comment=comment, user=request.user)
        liked = True
    
    return JsonResponse({'liked': liked, 'total_likes': comment.total_likes()})

def about(request):
    """
    View to display the about page.
    """
    return render(request, 'blog/about.html', {'title': 'About'})