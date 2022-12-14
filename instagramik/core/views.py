from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic import DetailView

from .models import CustomUser


class ProfileView(DetailView):
    model = CustomUser
    template_name = 'core/profile.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'profile'


class AddRemoveFriend(View):
    def post(self, request, user_id, *args, **kwargs):
        profile = get_object_or_404(CustomUser, id=user_id)
        if profile.friends.filter(id=request.user.id).exists():
            friend = profile.friends.get(id=request.user.id)
            profile.friends.remove(friend)
            request.user.friends.remove(profile)
        else:
            profile.friends.add(request.user)
            request.user.friends.add(profile)
        return redirect(request.META.get('HTTP_REFERER'), request)