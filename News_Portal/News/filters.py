import django_filters
from .models import Post, Author
import django.forms


class PostFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(
        field_name='title', label='Текст заголовка', lookup_expr='icontains',
        widget=django.forms.TextInput(
            attrs={'type': 'text', 'class': "form-control", 'placeholder': "Введите текст..."}))

    author = django_filters.ModelChoiceFilter(
        field_name='author', label='Выберите автора', queryset=Author.objects.all())

    date_time__gt = django_filters.DateFilter(
        field_name="add_date_time", label="От даты", lookup_expr='gt',
        widget=django.forms.DateInput(
            attrs={'type': 'date', 'class': "form-control"}))

    class Meta:
        model = Post
        # Порядок в словаре определяет порядок вывода полей в HTML
        fields = ['title', 'author', 'date_time__gt']

