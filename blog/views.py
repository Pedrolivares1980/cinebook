from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django import forms


def home(request):
    """View to render the home page with a list of posts."""
    context = {"posts": Post.objects.all()}
    return render(request, "blog/home.html", context)

def likeView(request, pk):
    post = get_object_or_404(Post, id=pk)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        # The user already liked this post.
        post.likes.remove(request.user)
        liked = False
    else:
        # A new like was added.
        post.likes.add(request.user)
        liked = True
    # Redirect back to the post detail view.
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

def commentLikeView(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    user_id = request.user.id if request.user.is_authenticated else 'Anonymous'

    commnet_liked = False
    if comment.likes.filter(id=request.user.id).exists():
        # The user has already liked this comment.
        comment.likes.remove(request.user)
        commnet_liked = False
    else:
        # A new like on the comment was added.
        comment.likes.add(request.user)
        commnet_liked = True

    return HttpResponseRedirect(reverse('post-detail', args=[str(comment.post.pk)]))

class PostListView(ListView):
    """View to display a list of blog posts."""

    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 5


class PostDetailView(DetailView):
    model = Post


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object 
        comments_list = Comment.objects.filter(post=post).order_by("-date_posted")

        # Paginate the comments list
        page = self.request.GET.get('page', 1)
        paginator = Paginator(comments_list, 5)  # Show 5 comments per page
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        liked = post.likes.filter(id=self.request.user.id).exists() if self.request.user.is_authenticated else False

        for comment in comments:
            comment.user_has_liked = comment.likes.filter(id=self.request.user.id).exists()

        context.update({
            'comments': comments,
            'total_likes': post.likes.count(),
            'liked': liked,
            'page_obj': comments,
        })

        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """View to create a new blog post."""

    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View to update an existing blog post."""

    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View to delete a blog post."""

    model = Post
    success_url = reverse_lazy("blog-home")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class CommentCreateView(LoginRequiredMixin, CreateView):
    """View to create a new comment on a blog post."""

    model = Comment
    fields = ["content"]
    template_name = "blog/add_comment.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['content'].widget = forms.Textarea(attrs={
            'rows': 8,
            'style': 'resize:none;',  
            'placeholder': 'Write your comment here...'
        })
        form.fields['content'].label = ''
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
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



class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ["content"]
    template_name = "blog/comment_update.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.object.post.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
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



def about(request):
    """
    View to display the about page.
    """
    return render(request, 'blog/about.html', {'title': 'About'})