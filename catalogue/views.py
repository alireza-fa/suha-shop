import convert_numbers
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from django.views.generic.detail import DetailView
from .models import Product, ProductComment, ProductFavorite, Category
from .forms import CommentForm
from django.http import JsonResponse
from permissions import RequiredLoginInPostMixin, LoginAndAdminRequiredMixin
from django.views import View
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator


# Todo: may be need to cache
class ProductDetailView(RequiredLoginInPostMixin, DetailView):
    model = Product
    template_name = 'catalogue/product_detail.html'
    class_form = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['colors'] = context['object'].colors.filter(count__gt=1)
        context['form'] = self.class_form()
        cats = context['object'].categories.all().values_list('category__id', flat=True)
        context['related_products'] = Product.objects.filter(categories__category__id__in=cats).exclude(id=context['object'].id).distinct()[:6]
        return context

    def post(self, request, slug):
        form = self.class_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            product = get_object_or_404(Product, slug=slug)
            ProductComment.objects.create(user=request.user, product=product, body=cd['body'], rate=cd['star'])
            string = render_to_string('catalogue/ajax/product_detail.html', {"form": self.class_form()})
            return JsonResponse(data={"status": 'ok', "data": string})
        string = render_to_string('catalogue/ajax/product_detail.html', {"form": form})
        return JsonResponse(data={"data": string})


class AddProductFavoriteView(LoginRequiredMixin, View):

    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        product_favorite = ProductFavorite.objects.filter(user=request.user, product=product)
        if product_favorite.exists():
            product_favorite.delete()
            return JsonResponse(data={"status": 'delete'})
        ProductFavorite.objects.create(user=request.user, product=product)
        return JsonResponse(data={"status": 'ok'})


@method_decorator(cache_page(900), name='dispatch')
class BestProductListView(ListView):
    model = Product
    template_name = 'catalogue/best_product_list.html'

    def get_queryset(self):
        return self.model.get_best_products()[:70]


@method_decorator(cache_page(900), name='dispatch')
class BoxListView(ListView):
    model = Product
    template_name = 'catalogue/box_list.html'

    def get_queryset(self):
        return self.model.objects.filter(is_box=True)[:70]


@method_decorator(cache_page(900), name='dispatch')
class SpecialProductListView(ListView):
    model = Product
    template_name = 'catalogue/special_list.html'

    def get_queryset(self):
        return self.model.objects.filter(is_special=True)[:70]


@method_decorator(cache_page(900), name='dispatch')
class CategoryProductListView(View):
    template_name = 'catalogue/category.html'

    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        return render(request, self.template_name, {"category": category})


class SearchProductView(View):
    template_name = 'catalogue/search_product.html'

    def get(self, request):
        q = request.GET.get('q')
        if q:
            products = Product.objects.filter(
                Q(title__icontains=q) | Q(description__icontains=q) | Q(brand__name=q) | Q(brand__english_name=q) |
                Q(upc__icontains=q)
            )
            return render(request, self.template_name, {"products": products, "q": q})
        return redirect('core:home')


class ProductFilterView(View):
    queryset = Product.objects.all()
    template_name = 'catalogue/ajax/filter.html'

    def post(self, request):
        self.queryset = self.queryset.filter(categories__category__id=request.POST.get('category'))
        brands = request.POST.getlist('brand[]')
        colors = request.POST.getlist('color[]')
        rates = request.POST.getlist('rates[]')
        minimum = request.POST.get('min')
        maximum = request.POST.get('max')
        if brands:
            self.queryset = self.queryset.filter(brand__id__in=brands).distinct()
        if colors:
            self.queryset = self.queryset.filter(colors__color__id__in=colors).distinct()
        if rates:
            self.queryset = self.queryset.filter(comments__rate__in=rates).distinct()
        if minimum:
            minimum = convert_numbers.persian_to_english(minimum)
            if minimum:
                self.queryset = self.queryset.filter(price__gte=minimum).distinct()
        if maximum:
            maximum = convert_numbers.persian_to_english(maximum)
            if maximum:
                self.queryset = self.queryset.filter(price__lte=maximum).distinct()
        string = render_to_string(self.template_name, {"products": self.queryset})
        alert = render_to_string('catalogue/ajax/alert_filter.html')
        return JsonResponse(data={"data": string, "status": 'ok', "alert": alert})


class CatalogueProfitView(LoginAndAdminRequiredMixin, View):
    template_name = 'catalogue/profit.html'

    def get(self, request):
        dictionary = Product.info()
        return render(request, self.template_name, dictionary)
