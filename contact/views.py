from django.shortcuts import render
from .forms import ContactForm
from profile.models import Profile
from blog.models import Article, Tag
from category.models import Category


def index(request):
    popular_posts = Article.objects.order_by('-views')[:3]
    categories = Category.objects.all()
    tags = Tag.objects.all()
    form = ContactForm(request.POST or None)
    author = Profile.objects.get(id=1)
    if form.is_valid():
        form.save()

    ctx = {
        'form': form,
        'author': author,
        'popular_posts': popular_posts,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'wordify/contact.html', ctx)
