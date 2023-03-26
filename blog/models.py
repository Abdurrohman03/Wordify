import string

from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify
from random import choice


class Tag(models.Model):
    title = models.CharField(max_length=225)

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=225)
    author = models.ForeignKey('profile.Profile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blogs/')
    category = models.ForeignKey('category.Category', on_delete=models.CASCADE, related_name='articles', null=True,
                                 blank=True)
    tags = models.ManyToManyField(Tag, related_name='articles')
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.slug is None:
            self.slug = slugify(self.title)
        try:
            super().save()
        except Exception as e:
            rand = "".join(choice(string.ascii_lowercase) for _ in range(4))
            self.slug = slugify(self.title) + f"-{rand}"
            super().save()


class Comments(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('profile.Profile', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        if self.author.user.get_full_name() != '':
            return f"{self.author.user.get_full_name()}' s comment"
        return f"{self.author.user.username}' s comment"

    class Meta:
        ordering = ['-id']


class SubContent(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.description


class SubImage(models.Model):
    image = models.ImageField(upload_to='subimage')
    subcontent = models.ForeignKey(SubContent, on_delete=models.CASCADE, related_name='subimage')
    is_white = models.BooleanField(default=False)
