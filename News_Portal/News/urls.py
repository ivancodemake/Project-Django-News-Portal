from django.urls import path
from .views import PostsList, PostDetail, SearchPosts
from .views import ArticleCreate, ArticleUpdate, ArticleDelete
from .views import NewsCreate, NewsUpdate, NewsDelete
from .views import start_page, CategoryListView, subscribe, del_subscribe
# from .views import IndexView

urlpatterns = [
   path('', start_page),
   # path('', IndexView.as_view()),
   path('news/', PostsList.as_view(), name='posts_list'),
   path('news/<int:pk>/', PostDetail.as_view(), name='post_detail'),
   path('search/', SearchPosts.as_view(), name='search_posts'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/create/', ArticleCreate.as_view(), name='article_create'),
   path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_update'),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/del_subscribe', del_subscribe, name='del_subscribe'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe')
]
