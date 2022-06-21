from django.urls import path
from . import views


app_name = 'basket'
urlpatterns = [
    path('', views.UserCartView.as_view(), name='cart'),
    path('add/<slug:slug>/', views.AddProductToCartView.as_view(), name='add_product'),
    path('checkout/', views.UserCheckoutView.as_view(), name='checkout'),
    path('change_quantity/<int:product_id>/', views.ChangeQuantity.as_view(), name='change_quantity'),
    path('remove_item/<int:product_id>/', views.RemoveItemView.as_view(), name='remove_item'),
]
