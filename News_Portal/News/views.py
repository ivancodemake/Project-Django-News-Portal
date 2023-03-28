from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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
    template_name = 'flatpages/News.html'
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


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostFormArticle
    model = Post
    template_name = 'flatpages/post_edit.html'
    permission_required = ('News.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = 'AR'
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Добавить статью"
        return context


class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostFormArticle
    model = Post
    template_name = 'flatpages/post_edit.html'
    permission_required = ('News.change_post',)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Редактировать статью"
        return context


class ArticleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'flatpages/post_delete.html'
    permission_required = ('News.delete_post',)
    success_url = reverse_lazy('posts_list')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Удаление статьи"
        context['previous_page_url'] = reverse_lazy('posts_list')
        return context


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostFormNews
    model = Post
    template_name = 'flatpages/post_edit.html'
    permission_required = ('News.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = 'NE'
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Добавить новость"
        return context


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostFormNews
    model = Post
    template_name = 'flatpages/post_edit.html'
    permission_required = ('News.change_post',)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Редактировать новость"
        return context


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'flatpages/post_delete.html'
    permission_required = ('News.delete_post',)
    success_url = reverse_lazy('posts_list')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Удаление новости"
        context['previous_page_url'] = reverse_lazy('posts_list')
        return context

