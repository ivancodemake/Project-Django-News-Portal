from django.contrib.auth.models import User
from django.db.models import Sum
from django.db import models


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        author_post_rating = self.post_set.aggregate(postRating=Sum('post_rating'))
        post_rate = 0
        post_rate += author_post_rating.get('postRating')

        author_comment_rating = self.user.comment_set.aggregate(commentRating=Sum('comment_rating'))
        comment_rate = 0
        comment_rate += author_comment_rating.get('commentRating')

        self.rating = 3 * post_rate + comment_rate
        self.save()

    def __str__(self):
        return f"{self.user}"


class Category(models.Model):
    name_cat = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name_cat}"


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    News = 'NE'
    Article = 'AR'
    type = [(Article, 'Статья'), (News, 'Новость')]

    category_type = models.CharField(max_length=2, choices=type, default=Article)
    add_date_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=256)
    text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:125]} + {"..."}'

    def __str__(self):
        data = 'Post from {}'.format(self.add_date_time.strftime('%d.%m.%Y %H:%M'))
        return f"{data},{self.author},{self.title}"


class PostCategory(models.Model):
    news = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.news},from the category:  {self.category}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

    def __str__(self):
        return f"{self.date_time}, {self.user}"
