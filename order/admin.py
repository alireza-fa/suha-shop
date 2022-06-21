from django.contrib import admin
from .models import Order, OrderItem, OrderItemColor


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product', )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_active', 'status', 'is_active', 'need_checkout', 'is_special')
    list_filter = ('is_active', 'status', 'is_special', 'need_checkout')
    search_fields = ('user__phone_number', 'ref_id', 'authority')
    inlines = (OrderItemInline, )
    raw_id_fields = ('user', )


@admin.register(OrderItemColor)
class OrderItemColorAdmin(admin.ModelAdmin):
    list_display = ('order_item', 'product_color', 'quantity')
