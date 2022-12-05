from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView

from .forms import PostCreateForm
from .models import Post


class IndexView(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = "posts"
    queryset = Post.objects.annotate(likes_count=Count('likes')).order_by('-likes_count')[:10]


# def index(request):
#     post_query = Post.objects.annotate(likes_count=Count('likes')).order_by('-likes_count')[:10]
#     context = {
#         'posts': post_query,
#     }
#     return render(request, 'posts/index.html', context)


class FeedView(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = "posts"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Post.objects.filter(author__in=self.request.user.friends.all()).order_by('-date_pub')[:10]
        else:
            queryset = []
        return queryset


# class FeedView(View):
#     template_name = 'posts/index.html'
#
#     def get(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             posts = Post.objects.filter(author__in=request.user.friends.all()).order_by('-date_pub')[:10]
#             context = {
#                 'posts': posts,
#             }
#             return render(request, self.template_name, context)
#         else:
#             return render(request, self.template_name)


# def feed(request):
#     current_user = request.user
#     post_query = Post.objects.all()
#
#     if current_user and current_user.is_authenticated:
#         post_query = post_query.filter(author__in=current_user.friends.all())
#
#     output = ["Post #{}: {} likes".format(post.id, post.like_count) for post in post_query]
#     return HttpResponse(output)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required()
def post_create(request):
    template_name = 'posts/post_create.html'
    if request.method == 'GET':
        form = PostCreateForm()
        context = {'form': form}
        return render(request, template_name, context)
    elif request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(reverse('posts:post_detail', kwargs={'post_id': post.id}))
        else:
            context = {'form': form}
            return render(request, template_name, context)



def post_edit(request, post_id):
    response = "Post edit #{}".format(post_id)
    return HttpResponse(response)


def post_delete(request, post_id):
    response = "Post delete #{}".format(post_id)
    return HttpResponse(response)


def post_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user and request.user.is_authenticated:
        if request.user in post.likes.all():
            like = post.likes.get(pk=request.user.id)
            post.likes.remove(like)
        else:
            post.likes.add(request.user)
            post.save()
    return redirect(request.META.get('HTTP_REFERER'), request)
