from django.db import models
from django.urls import reverse


class CategoryModel(models.Model):
	title = models.CharField(max_length=100)
	slug = models.SlugField(max_length=100, unique=True)

	class Meta:
		ordering = ['title']
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('catalog:products_by_category', args=[self.slug])


class ProductModel(models.Model):
	category = models.ForeignKey(CategoryModel, related_name='products', on_delete=models.PROTECT)
	title = models.CharField(max_length=100)
	slug = models.SlugField(max_length=100)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	stock = models.PositiveIntegerField()
	availible = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['title']
		verbose_name = 'Продукт'
		verbose_name_plural = 'Продукты'

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('catalog:product_detail', args=[self.id])

