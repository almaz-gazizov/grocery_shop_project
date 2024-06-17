from django.contrib import admin

from shop.models import (
    Category,
    Product,
    Subcategory,
    ShoppingCart
)


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1


class SubCategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    inlines = [SubCategoryInline]


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    inlines = [ProductInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category',
        'subcategory', 'price', 'image_small'
    )
    list_display_links = ('name',)
    list_filter = ('category', 'subcategory')
    search_fields = ('name',)
    list_editable = ('price',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_display_links = ('user',)
    search_fields = ('user',)
    empty_value_display = 'Не задано'
