from django.urls import path
from . import views


app_name = 'catalogue'
urlpatterns = [
    path('product/favorite/add_or_delete/<slug:slug>/', views.AddProductFavoriteView.as_view(), name='add_product_to_favorite'),
    path('product/best_products/', views.BestProductListView.as_view(), name='best_products'),
    path('product/boxes/', views.BoxListView.as_view(), name='boxes'),
    path('product/special_product/', views.SpecialProductListView.as_view(), name='special_products'),
    path('product/category/<slug:slug>/', views.CategoryProductListView.as_view(), name='category_products'),
    path('product/detail/<slug:slug>/', views.ProductDetailView.as_view(), name='detail'),
    path('product/search/', views.SearchProductView.as_view(), name='search_product'),
    path('product/filters/', views.ProductFilterView.as_view(), name='filters'),
    path('profit/', views.CatalogueProfitView.as_view(), name='profit'),
]
