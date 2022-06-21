from django.contrib import admin
from catalogue.models import Category, Brand, BrandCategory, Product, ProductCategory, ProductColor, \
    ProductImage, ProductFavorite, ProductComment, Color, Discount


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('is_child', )
    prepopulated_fields = {'slug': ('english_name', )}
    search_fields = ('name', )
    raw_id_fields = ('parent', )


class BrandCategoryInline(admin.TabularInline):
    model = BrandCategory
    extra = 1
    raw_id_fields = ('category', )


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', )
    prepopulated_fields = {'slug': ('english_name', )}
    search_fields = ('name', )
    inlines = (BrandCategoryInline, )


class ProductCategoryInline(admin.TabularInline):
    model = ProductCategory
    extra = 1
    raw_id_fields = ('category', )


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    prepopulated_fields = {"slug": ('english_name', )}


class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 3
    raw_id_fields = ('color', )


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'count', 'is_active', 'discount', 'is_new', 'is_special')
    list_filter = ('is_active', 'is_new', 'is_special')
    list_editable = ('is_active', 'is_new', 'is_special')
    search_fields = ('title', 'description', 'brand__name')
    inlines = (ProductCategoryInline, ProductColorInline, ProductImageInline)
    prepopulated_fields = {'slug': ('english_title', )}


@admin.register(ProductFavorite)
class ProductFavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')


@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rate', 'is_read', 'is_active')
    list_filter = ('is_read', 'is_active', 'rate')
    list_editable = ('is_read', 'is_active')
    search_fields = ('user__username', 'product__title')


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_active', 'is_limit', 'is_private', 'time_use')
    list_filter = ('is_active', 'is_limit', 'is_private')
    search_fields = ('code', )
    list_editable = ('is_active', 'is_limit', 'is_private')
