from django import template
from catalogue.models import ProductColor


register = template.Library()


@register.filter(name='is_favorite')
def get_is_favorite_product(value, user):
    return user.favorites.filter(product=value).exists()


@register.filter(name='is_active')
def is_active_product(query):
    return query.filter(product__is_active=True)[:100]


@register.filter(name='brands')
def get_brands_filter(category):
    queryset = category.brands.all()
    if not queryset and category.is_child:
        queryset = category.parent.brands.all()
        if not queryset and category.parent.is_child:
            queryset = category.parent.parent.brands.all()
    return queryset


@register.filter(name='colors')
def get_colors_filter(category):
    return ProductColor.objects.filter(product__categories__category=category)
