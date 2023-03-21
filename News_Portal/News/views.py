from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from .forms import PostFormArticle, PostFormNews
from .models import Post
from .filters import PostFilter


def start_page(request):
    return render(request, 'flatpages/start.html')


class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/post.html'
    context_object_name = 'post'


class PostsList(ListView):
    paginate_by = 10
    model = Post
    ar_ne = "category_type"
    ordering = '-add_date_time'
    template_name = 'flatpages/news.html'
    context_object_name = 'posts'


class SearchPosts(ListView):
    paginate_by = 10
    model = Post
    ordering = '-add_date_time'
    template_name = 'flatpages/search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['search_filter'] = self.filterset
        return context


class ArticleCreate(CreateView):
    form_class = PostFormArticle
    model = Post
    template_name = 'flatpages/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = 'AR'
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Добавить статью"
        return context


class ArticleUpdate(UpdateView):
    form_class = PostFormArticle
    model = Post
    template_name = 'flatpages/post_edit.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Редактировать статью"
        return context


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('posts_list')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Удаление статьи"
        context['previous_page_url'] = reverse_lazy('posts_list')
        return context


class NewsCreate(CreateView):
    form_class = PostFormNews
    model = Post
    template_name = 'flatpages/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = 'NE'
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Добавить новость"
        return context


class NewsUpdate(UpdateView):
    form_class = PostFormNews
    model = Post
    template_name = 'flatpages/post_edit.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Редактировать новость"
        return context


class NewsDelete(DeleteView):
    model = Post
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('posts_list')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Удаление новости"
        context['previous_page_url'] = reverse_lazy('posts_list')
        return context

