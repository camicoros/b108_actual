from django.urls import path, re_path
from . import views


app_name = 'posts'

urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name="index"),
    path('posts/create/', views.post_create, name="post_create"),
    path('posts/<int:post_id>/delete/', views.post_delete, name="post_delete"),
    path('posts/<int:post_id>/edit/', views.post_edit, name="post_edit"),
    path('posts/<int:post_id>/like/', views.post_like, name="post_like"),
    re_path(r'^posts/(?P<post_id>\w+)/$', views.post_detail, name="post_detail"),
    path('feed/', views.FeedView.as_view(), name="feed"),
]