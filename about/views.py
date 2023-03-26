from django.shortcuts import render
from blog.models import Article, Tag
from category.models import Category
from profile.models import Profile


def index(request):
    popular_posts = Article.objects.order_by('-views')[:3]
    categories = Category.objects.all()
    tags = Tag.objects.all()
    author = Profile.objects.get(id=1)
    article_list = Article.objects.order_by('-id')
    ctx = {
        'author': author,
        'popular_posts': popular_posts,
        'categories': categories,
        'tags': tags,
        'object_list': article_list
    }
    return render(request, 'wordify/about.html', ctx)
