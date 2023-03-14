from django.shortcuts import render
from django.views.generic.base import View
from .models import *


class PostDetail(View):
    def get(self, request, pk):
        ps = Post.objects.get(id=pk)
        return render(request, "flatpages/posts.html", {'ps': ps})


def news_page_list(request):
    newslist = Post.objects.all().order_by('-add_date_time')
    return render(request, 'flatpages/News.html', {'newslist': newslist})


def start_page(request):
    return render(request, 'flatpages/start.html')

