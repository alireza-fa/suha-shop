from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from catalogue.models import Product, Discount, ProductColor


def delete_user():
    return User.objects.get_or_create(phone_number='09111111111', username='delete', password='delete')[0]


class OrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('items')


class OrderItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('product', 'order')


class Order(models.Model):
    NOT_PAID = 0
    PAID = 1
    PACK = 2
    SHIP = 3
    DONE = 4

    ORDER_STATUS = (
        (NOT_PAID, 'پرداخت نشده'),
        (PAID, 'سفارش ثبت شده'),
        (PACK, 'بسته بندی محصول'),
        (SHIP, 'حمل کالا'),
        (DONE, 'تحویل داده شده')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name=_('user'))
    authority = models.CharField(max_length=220, null=True, blank=True, verbose_name=_('authority'))
    ref_id = models.CharField(max_length=220, null=True, blank=True, verbose_name=_('ref id'))
    status = models.PositiveSmallIntegerField(choices=ORDER_STATUS, verbose_name=_('status'))
    discount_code = models.CharField(max_length=18, null=True, blank=True, verbose_name=_('discount code'))
    is_active = models.BooleanField(default=True)
    need_checkout = models.BooleanField(default=False, verbose_name=_('need checkout'))
    is_special = models.BooleanField(default=False, verbose_name=_('is special'))
    special_price = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('special price'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified'))

    default_manager = models.Manager()
    objects = OrderManager()

    class Meta:
        ordering = ('-created', )
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return 'order'

    def get_total_price(self):
        total = sum(item.get_price() for item in self.items.all())
        discount = self.get_discount()
        if discount:
            discount_mount = total * discount // 100
            return total - discount_mount
        return total

    def get_discount(self):
        if self.discount_code:
            discount = Discount.objects.filter(code=self.discount_code)
            if discount.exists():
                return discount.first().discount
        return None

    def save_product(self):
        items = self.items.all()
        for item in items:
            item.product.purchase_count += item.quantity
            if item.product.purchase_count >= item.product.count:
                item.product.is_active = False
            item.product.save()
            for item_product_col in item.product_colors.all():
                count = item_product_col.product_color.count - item_product_col.quantity
                if count >= 0:
                    item_product_col.product_color.count -= item_product_col.quantity
                    item_product_col.product_color.save()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('order:detail', args=[self.id])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('order'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders', verbose_name=_('product'))
    quantity = models.PositiveSmallIntegerField(verbose_name=_('quantity'))

    default_manager = models.Manager()
    objects = OrderItemManager()

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')

    def __str__(self):
        return f'{self.order} - {self.product}'

    def get_price(self):
        return self.product.get_price() * self.quantity


class OrderItemColor(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='product_colors', verbose_name=_('order oitem'))
    product_color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, related_name='order_items', verbose_name=_('product color'))
    quantity = models.PositiveSmallIntegerField(verbose_name=_('quantity'), default=1)

    class Meta:
        verbose_name = _('order item color')
        verbose_name_plural = _('order item colors')

    def __str__(self):
        return self.order_item
