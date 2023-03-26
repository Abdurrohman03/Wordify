from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Article, Tag
from category.models import Category
from .forms import CommentForm
from profile.models import Profile
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework


def index(request):
    carousel_list = Article.objects.order_by('-id')[:3]
    articles = Article.objects.order_by('-id')
    author = Profile.objects.get(id=1)
    popular_posts = Article.objects.order_by('-views')[:3]
    categories = Category.objects.all()
    tags = Tag.objects.all()
    page_number = request.GET.get('page', 1)
    paginator = Paginator(articles, 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(1)
    ctx = {
        'carousel_list': carousel_list,
        'object_list': page_obj,
        'author': author,
        'popular_posts': popular_posts,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'wordify/index.html', ctx)


def detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    article.views += 1
    article.save()
    related_posts = Article.objects.filter(category=article.category)[:3]
    popular_posts = Article.objects.order_by('-views')[:3]
    categories = Category.objects.all()
    tags = Tag.objects.all()
    author = Profile.objects.get(id=1)
    object_categories = Category.objects.filter(articles=article)
    object_tags = Tag.objects.filter(articles=article)
    form = CommentForm()
    if request.method == 'POST':

        if not request.user.is_authenticated:

            return redirect('profile:login')
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author_id = request.user.profile.id
            comment.article_id = article.id
            comment.save()
            return redirect('.')
    ctx = {
        'object': article,
        'author': author,
        'object_categories': object_categories,
        'object_tags': object_tags,
        'form': form,
        'popular_posts': popular_posts,
        'categories': categories,
        'tags': tags,
        'related_posts': related_posts,
    }
    return render(request, 'wordify/blog-single.html', ctx)


def article_list(request):
    author = Profile.objects.get(id=1)
    articles = Article.objects.order_by('-id')
    popular_posts = Article.objects.order_by('-views')[:3]
    categories = Category.objects.all()
    tags = Tag.objects.all()
    search = request.GET.get('search')
    cat = request.GET.get('cat')
    tag = request.GET.get('tag')
    if search:
        articles = articles.filter(title__icontains=search)
    if cat:
        articles = articles.filter(category__title__exact=cat)
    if tag:
        articles = articles.filter(tags__title__exact=tag)
    page_number = request.GET.get('page', 1)
    paginator = Paginator(articles, 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(1)
    ctx = {
            'title': search,
            'cat': cat,
            'author': author,
            'tag': tag,
            'popular_posts': popular_posts,
            'categories': categories,
            'tags': tags,
            'object_list': page_obj,
    }
    return render(request, 'wordify/list.html', ctx)


class