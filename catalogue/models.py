from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from accounts.models import User
from django.utils import timezone
from django.db.models import Sum, Q, Avg, Count
from .managers import IsActiveManager, DiscountManager


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True, verbose_name=_('name'))
    english_name = models.CharField(max_length=120, unique=True, verbose_name=_('english name'))
    slug = models.SlugField(max_length=120, unique=True, verbose_name=_('slug'), allow_unicode=True)
    image = models.ImageField(verbose_name=_('image'), default='category.jpg')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                               verbose_name=_('parent'))
    is_child = models.BooleanField(default=False, verbose_name=_('is child'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('catalogue:category_products', args=[self.slug])


class Brand(models.Model):
    name = models.CharField(max_length=120, unique=True, verbose_name=_('brand'))
    english_name = models.CharField(max_length=120, unique=True, verbose_name=_('english name'))
    slug = models.SlugField(max_length=120, unique=True, verbose_name=_('slug'), allow_unicode=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))

    class Meta:
        verbose_name = _('brand')
        verbose_name_plural = _('brands')

    def __str__(self):
        return self.name


class BrandCategory(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='categories', verbose_name=_('brand'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='brands', verbose_name=_('category'))

    class Meta:
        verbose_name = _('brand category')
        verbose_name_plural = _('brand categories')

    def __str__(self):
        return f'{self.brand} - {self.category}'


class Product(models.Model):
    upc = models.IntegerField(unique=True, verbose_name=_('upc code'))
    title = models.CharField(max_length=240, unique=True, verbose_name=_('title'))
    english_title = models.CharField(max_length=240, unique=True, verbose_name=_('english title'))
    slug = models.SlugField(max_length=240, unique=True, verbose_name=_('slug'), allow_unicode=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True, related_name=_('brand'), verbose_name=_('brand'))
    count = models.PositiveSmallIntegerField(verbose_name=_('count'))
    purchase_count = models.PositiveSmallIntegerField(default=0, verbose_name=_('purchase count'))
    description = RichTextField(verbose_name=_('description'))
    meta_description = models.CharField(max_length=200, verbose_name=_('meta description'))
    price_for_me = models.PositiveIntegerField(verbose_name=_('price for me'))
    price = models.PositiveIntegerField(verbose_name=_('price'))
    image = models.ImageField(verbose_name=_('image'))
    video = models.FileField(verbose_name=_('video'), null=True, blank=True)
    discount = models.PositiveSmallIntegerField(
        validators=[validators.MinValueValidator(1), validators.MaxValueValidator(100)], null=True, blank=True,
        verbose_name=_('discount')
    )
    discount_time = models.DateTimeField(null=True, blank=True, verbose_name=_('discount expire'))
    is_box = models.BooleanField(default=False, verbose_name=_('is box'))
    is_new = models.BooleanField(default=True, verbose_name=_('is new'))
    is_special = models.BooleanField(default=False, verbose_name=_('is special'))
    is_colorful = models.BooleanField(default=False, verbose_name=_('is colorful'))
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    created = models.DateTimeField(auto_now_add=True, verbose_name='created')
    updated = models.DateTimeField(auto_now=True, verbose_name=_('updated'))\

    default_manager = models.Manager()
    objects = IsActiveManager()

    class Meta:
        ordering = ('-created', )
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return f'{self.title[:30]} - {self.count}'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('catalogue:detail', args=[self.slug])

    def get_price(self):
        now = timezone.now()
        if self.discount and self.discount_time > now:
            discount = (self.discount * self.price) // 100
            return self.price - discount
        return self.price

    def percent_sale(self):
        all_purchase_count = self.count
        count = self.purchase_count
        percent = (count * 100) // all_purchase_count
        return percent

    def get_rate(self):
        rate = self.comments.filter(is_active=True).aggregate(avg=Avg('rate'), count=Count('rate'))
        if rate['avg']:
            rate['avg'] = int(rate['avg'])
        return rate

    def get_comments(self):
        return self.comments.filter(is_active=True)

    @classmethod
    def get_best_products(cls):
        return cls.objects.all().annotate(avg_rate=Avg('comments__rate')).order_by('avg_rate')

    @classmethod
    def get_discount_products(cls):
        now = timezone.now()
        return cls.objects.filter(discount__isnull=False, discount_time__gte=now).order_by('-discount')

    @classmethod
    def info(cls):
        products = cls.objects.all()
        profit = sum([product.get_price() * abs((product.count - product.purchase_count)) for product in products])
        count = sum([product.count - product.purchase_count for product in products])
        return {"products": products, "profit": profit, "count": count}


class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='categories',
                                verbose_name=_('categories'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products',
                                 verbose_name=_('products'))

    class Meta:
        verbose_name = _('products category')
        verbose_name_plural = _('products categories')

    def __str__(self):
        return f'{self.product.title[:20]} - {self.category}'


class Color(models.Model):
    name = models.CharField(max_length=32, verbose_name=_('color'))
    english_name = models.CharField(max_length=32, verbose_name=_('english name'))
    slug = models.SlugField(max_length=32, verbose_name=_('slug'))
    code = models.CharField(max_length=32, verbose_name=_('code'))

    class Meta:
        verbose_name = _('Color')
        verbose_name_plural = _('Colors')

    def __str__(self):
        return f'{self.name} - {self.code}'


class ProductColor(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors', verbose_name=_('colors'))
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='colors', verbose_name=_('products'))
    count = models.PositiveSmallIntegerField(verbose_name=_('count'))

    class Meta:
        verbose_name = _('product color')
        verbose_name_plural = _('product colors')

    def __str__(self):
        return f'{self.product.title[:20]} - {self.color}'


class ProductImage(models.Model):
    name = models.CharField(max_length=120, verbose_name=_('name'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name=_('product'))
    image = models.ImageField(verbose_name=_('image'))

    class Meta:
        verbose_name = _('product image')
        verbose_name_plural = _('product images')

    def __str__(self):
        return f'{self.name[:30]} - {self.product.title[:30]}'


class ProductFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name=_('user'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites', verbose_name=_('product'))

    class Meta:
        verbose_name = _('product favorite')
        verbose_name_plural = _('product favorites')

    def __str__(self):
        return f'{self.user} - {self.product.title[:30]}'


class ProductComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name=_('user'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name=_('product'))
    body = models.TextField(verbose_name=_('body'))
    rate = models.PositiveIntegerField(
        validators=[validators.MinValueValidator(1), validators.MaxValueValidator(5)], verbose_name=_('rate')
    )
    is_read = models.BooleanField(default=False, verbose_name=_('is read'))
    is_active = models.BooleanField(default=False, verbose_name=_('is active'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('updated'))

    default_manager = models.Manager()
    objects = IsActiveManager()

    class Meta:
        ordering = ('-created', )
        verbose_name = _('product comment')
        verbose_name_plural = _('product comments')

    def __str__(self):
        return f'{self.user} - {self.product.title[:30]}'


class Discount(models.Model):
    code = models.CharField(max_length=18, unique=True, verbose_name=_('code'))
    discount = models.PositiveSmallIntegerField(verbose_name=_('discount'))
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    expire_time = models.DateTimeField(verbose_name=_('expire time'))
    is_limit = models.BooleanField(default=False, verbose_name=_('is have limit'))
    time_use = models.PositiveSmallIntegerField(verbose_name=_('time for use'), null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False, verbose_name=_('is private'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discounts', verbose_name=_('user'), null=True, blank=True)

    default_manager = models.Manager()
    objects = DiscountManager()

    class Meta:
        ordering = ('-expire_time', )
        verbose_name = _('Discount')
        verbose_name_plural = _('Discounts')

    def __str__(self):
        return self.code
