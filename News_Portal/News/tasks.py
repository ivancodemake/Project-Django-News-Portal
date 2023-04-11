from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from News.models import Post, Category
from News_Portal import settings
from celery import shared_task
import datetime


@shared_task
def notify_new_post_with_celery(pk):
    post = Post.objects.get(id=pk)
    subscribers_list = []
    categories_current_post = post.category.all()

    for category in categories_current_post:
        for user in category.subscribers.all():
            subscribers_list.append(user)

    for i in subscribers_list:
        user = i.username
        e_mail = i.email

        html_content = render_to_string('post_created_email.html', {'link': f'{settings.SITE_URL}/news/{pk}'})

        msg = EmailMultiAlternatives(
            subject=f'Новый пост: {post.title}',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[e_mail],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def weekly_sends():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(add_date_time__gte=last_week)
    categories = set(posts.values_list('category__name_cat', flat=True))
    subscribers = set(Category.objects.filter(name_cat__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
