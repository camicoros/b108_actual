from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import Post


def index(request):
    post_query = Post.objects.annotate(likes_count=Count('likes')).order_by('-likes_count')[:10]
    template = loader.get_template('posts/index.html')
    context = {
        'posts': post_query,
    }
    return HttpResponse(template.render(context))


def feed(request):
    current_user = request.user
    post_query = Post.objects.all()

    if current_user and current_user.is_authenticated:
        post_query = post_query.filter(author__in=current_user.friends.all())

    output = ["Post #{}: {} likes".format(post.id, post.like_count) for post in post_query]
    return HttpResponse(output)


def post_detail(request, post_id):
    response = "Post #{}".format(post_id)
    return HttpResponse(response)


def post_create(request):
    response = "Post create"
    return HttpResponse(response)


def post_edit(request, post_id):
    response = "Post edit #{}".format(post_id)
    return HttpResponse(response)


def post_delete(request, post_id):
    response = "Post delete #{}".format(post_id)
    return HttpResponse(response)


def post_like(request, post_id):
    response = "Post like #{}".format(post_id)
    return HttpResponse(response)