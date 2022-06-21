from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BasketConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'basket'
    verbose_name = _('Basket')
