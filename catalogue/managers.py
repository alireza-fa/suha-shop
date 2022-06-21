from django.db.models import Manager
from django.utils import timezone


class IsActiveManager(Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).select_related('brand').prefetch_related('categories', 'comments')


class DiscountManager(Manager):

    def get_queryset(self):
        now = timezone.now()
        return super().get_queryset().filter(is_active=True, expire_time__gte=now)


class ProductColorManager(Manager):
    def get_queryset(self):
        return self.get_queryset().filter(count__gt=0)
