from decimal import Decimal
from django.conf import settings
from catalog.models import ProductModel


class Cart:
	"""
    Класс описывающий свойства и методы корзины покупателя:
     * Инициализация корзины;
     * Добавление товаров в корзину;
     * Удаление товаров из корзины;
     * Обновление корзины после изменений;
     * Возврат конечной суммы всех элементов корзины;
     * Очистка корзины;
     * Служебные методы - итератор и кол-во элементов корзины
    """
	def __init__(self, request):
		"""
        Инициализация корзины: проверяет наличие корзины в сессии и
        создаёт корзину при отсутствии сессии.

        :request: объект request django из уровня представления
        """
		self.session = request.session
		cart = self.session.get(settings.CART_SESSION_ID)
		if not cart:
			cart = self.session[settings.CART_SESSION_ID] = {}
		self.cart = cart


	def add(self, product, quantity=1, update_quantity=False):
		"""
		Добавление продукта: проверяет наличие товара в корзине;
		при наличие товара в корзине увеличивает значение количества.

		:product: обект модели Product, описывающий продукт или товар;
		:quantity: кол-во продукта или товара, которое необходимо внести
		в корзину
		:update quantity: логический аргумент; при значении True - количество
		перезаписвается на указанное, при значение False - количество добавляется
		к уже существующему.
		"""
		product_id = str(product.id)
		if product_id not in self.cart:
			self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
		if update_quantity:
			self.cart[product_id]['quantity'] = quantity
		else:
			self.cart[product_id]['quantity'] += quantity
		self.save()


	def remove(self, product):
		"""
		Удаление продукта: удаляет продукт из корзины, если такой существует там.

		:product: обект модели Product, описывающий продукт или товар;
		"""
		product_id = str(product.id)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()


	def save(self):
		"""
		Сохраняет изменения в сессии после всех изменений.
		"""
		self.session[settings.CART_SESSION_ID] = self.cart
		self.session.modified = True


	def __iter__(self):
		"""
		Служебный метод, предназначенный для возможности проитеррировать корзину.
		"""
		products_id = self.cart.keys()
		products = ProductModel.objects.filter(id__in=products_id)
		
		for product in products:
			self.cart[str(product.id)]['product'] = product

		for item in self.cart.values():
			item['price'] = Decimal(item['price'])
			item['total_price'] = item['price'] * item['quantity']
			yield item


	def __len__(self):
		"""
		Служебный метод, возвращающий кол-во элементов в корзине.
		"""
		return sum(item['quantity'] for item in self.cart.values())


	def get_total_price(self):
		"""
		Метод, возвращает общую стоимость всех элементов корзины.
		"""
		return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())


	def clear(self):
		"""
		Метод удаляет корзину из сессии.
		"""
		del self.session[settings.CART_SESSION_ID]
		self.session.modified = True
