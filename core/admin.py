from django.contrib import admin
from .models import Contact, Slider, SiteSetting


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'read', 'active', 'created')
    list_filter = ('read', 'active')
    search_fields = ('phone_number', 'name')


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title', )
    raw_id_fields = ('product', )


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    pass
