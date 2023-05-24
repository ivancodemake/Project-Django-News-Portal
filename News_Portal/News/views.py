from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from .forms import PostFormArticle, PostFormNews
from .models import Post, Category
from .filters import PostFilter
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.core.cache import cache  # импортируем наш кэш


def start_page(request):
    return render(request, 'flatpages/start.html')


class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/post.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.
        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)
        return obj


class PostsList(ListView, View):
    paginate_by = 10
    model = Post
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


class CategoryListView(ListView):
    paginate_by = 10
    model = Post
    template_name = 'flatpages/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-add_date_time')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории - '
    return render(request, 'flatpages/subscribe.html', {'category': category, 'message': message})


@login_required
def del_subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)

    message = 'Вы успешно отписались от рассылки новостей категории - '
    return render(request, 'flatpages/subscribe.html', {'category': category, 'message': message})



