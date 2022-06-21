from django.contrib import admin
from .models import Category, Post, PostComment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )
    prepopulated_fields = {"slug": ('english_name', )}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'is_active')
    list_filter = ('category', 'is_active', 'author')
    list_editable = ('is_active', )
    search_fields = ('title', 'author__username', 'body', 'category__name')
    prepopulated_fields = {"slug": ('english_title', )}


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'is_read', 'is_active')
    list_filter = ('is_read', 'is_active')
    search_fields = ('post__title', 'user__username', 'post__id')
