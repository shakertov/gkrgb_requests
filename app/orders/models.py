from django.db import models
from catalog.models import ProductModel


class OrderModel(models.Model):
	first_name = models.CharField(max_length=50, verbose_name='Ваше Имя')
	last_name = models.CharField(max_length=50, verbose_name='Ваша Фамилия')
	email = models.EmailField(verbose_name='Ваш Email')
	address = models.CharField(max_length=250, verbose_name='Адрес')
	city = models.CharField(max_length=50, verbose_name='Город')
	comment = models.TextField(verbose_name='Комментарий')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	paid = models.BooleanField(default=False)

	class Meta:
		ordering = ['-created']
		verbose_name = 'Заказ'
		verbose_name_plural = 'Заказы'

	def __str__(self):
		return 'Заказ номер - ' + str(self.id)


class OrderItemModel(models.Model):
	order = models.ForeignKey(OrderModel, related_name='items', on_delete=models.PROTECT)
	product = models.ForeignKey(ProductModel, related_name='order_items', on_delete=models.PROTECT)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField(default=1)

	def __str__(self):
		return str(self.id)

	def get_cost(self):
		return self.price * self.quantity
