from django.contrib import admin


# Импорт с приложения
from catalog.models import CategoryModel, ProductModel


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['title', 'slug']


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
	list_display = [
		'title', 'slug', 'price',
		'stock', 'availible', 'created', 'updated'
	]
	list_filter = ['availible', 'created', 'updated']
	list_editable = ['price', 'stock', 'availible']