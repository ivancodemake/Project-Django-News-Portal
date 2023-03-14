from django.urls import path
from .views import *

urlpatterns = [
   path('', start_page),
   path('news/', news_page_list),
   path('news/<int:pk>/', PostDetail.as_view()),
]
