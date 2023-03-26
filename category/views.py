from django.shortcuts import render
from blog.models import Article, Tag
from .models import Category
from profile.models import Profile
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def index(request):
    articles = Article.objects.order_by('-id')
    cat = request.GET.get('cat')
    popular_posts = Article.objects.order_by('-views')[:3]
    author = Profile.objects.get(id=1)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    if cat:
        articles = articles.filter(category__title__icontains=cat)
    page_number = request.GET.get('page', 1)
    paginator = Paginator(articles, 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(1)
    ctx = {
        'object_list': page_obj,
        'cat': cat,
        'author': author,
        'popular_posts': popular_posts,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'wordify/category.html', ctx)
