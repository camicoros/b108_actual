from django.shortcuts import render
from django.http import HttpResponse


def index1(request, post_id=0):
    print(request)
    print(post_id)
    return HttpResponse("hello! {}".format(post_id))


def index2(request):
    return HttpResponse("goodbye!")