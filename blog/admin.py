from django.contrib import admin
from .models import Tag, Article, Comments, SubContent, SubImage


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'created_date']
    date_hierarchy = 'created_date'
    list_display_links = ['id', 'title']
    search_fields = ['title', 'author__username', 'author__first_name', 'author__last_name', 'category']
    filter_horizontal = ['tags']
    ordering = ['-id']


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_date']
    search_fields = ['article', 'author__username', 'author__first_name', 'author__last_name']


admin.site.register(SubContent)
admin.site.register(SubImage)

