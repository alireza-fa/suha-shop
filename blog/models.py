from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from accounts.models import User


class IsActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Category(models.Model):
    name = models.CharField(max_length=32, verbose_name=_('name'))
    english_name = models.CharField(max_length=32, verbose_name=_('english name'))
    slug = models.SlugField(max_length=32, verbose_name=_('slug'), unique=True)
    image = models.ImageField(verbose_name=_('image'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))

    class Meta:
        ordering = ('-created', )
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:category_list', args=[self.slug])


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', verbose_name=_('category'))
    title = models.CharField(max_length=120, verbose_name=_('title'))
    english_title = models.CharField(max_length=120, verbose_name=_('english title'))
    slug = models.SlugField(max_length=120, verbose_name=_('slug'), unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name=_('author'))
    time_to_read = models.CharField(max_length=32, verbose_name=_('time to read'))
    meta_description = models.CharField(max_length=200, verbose_name=_('meta description'))
    image = models.ImageField(verbose_name=_('image'))
    image_detail = models.ImageField(verbose_name=_('image for detail'), null=True)
    body = RichTextField(verbose_name=_('body'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified'))
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))

    default_manager = models.Manager()
    objects = IsActiveManager()

    class Meta:
        ordering = ('-created', )
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:detail', args=[self.slug])


class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name=_('post'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comments', verbose_name=_('user'))
    message = models.TextField(verbose_name=_('message'))
    is_read = models.BooleanField(default=False, verbose_name=_('is read'))
    is_active = models.BooleanField(default=False, verbose_name=_('is active'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True)

    default_manager = models.Manager()
    objects = IsActiveManager()

    class Meta:
        ordering = ('-created', )
        verbose_name = _('Post comment')
        verbose_name_plural = _('Post Comments')

    def __str__(self):
        return f'{self.post} - {self.user}'
