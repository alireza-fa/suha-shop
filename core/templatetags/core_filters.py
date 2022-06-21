from django import template
from catalogue.models import Product, Category
from core.models import Slider
from blog.models import Category as PostCategory


register = template.Library()


@register.filter(name='home_filter')
def home_filter(value):
    if value == 'sliders':
        return Slider.objects.all()[:4]
    elif value == 'category':
        return Category.objects.filter(is_child=False)
    elif value == 'discount_product':
        return Product.get_discount_products()[:8]
    elif value == 'best_product':
        return Product.get_best_products()[:8]
    elif value == 'box':
        return Product.objects.filter(is_box=True)[:4]
    elif value == 'special_product':
        return Product.objects.filter(is_special=True).order_by('?')[:4]


@register.filter(name='blog_filter')
def blog_filter(value):
    if value == 'category':
        return PostCategory.objects.all()
