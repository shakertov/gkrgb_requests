from django.shortcuts import render, redirect, get_object_or_404
from orders.models import OrderItemModel, OrderModel
from orders.forms import OrderForm
from cart.cart import Cart
from cart.forms import CartAddProductForm
from catalog.models import ProductModel
from django.contrib import messages
from django.db.models import F, Sum


def order_prepare(request):
	if request.session.get('order_created_id'):
		msg = 'Пожалуйста, сначала закончите с оформлением этой заявки! Либо отмените её - ссылка представлена ниже.'
		messages.add_message(request, messages.INFO, msg)
		return redirect('orders:order_create')
	products = ProductModel.objects.filter(availible=True)
	form = CartAddProductForm()

	data = {
		'products': products,
		'form': form
	}
	return render(request, 'catalog/list.html', data)


def order_create(request):
	if request.session.get('order_created_id'):
		# Вывести небольшой чек с данными из заказа
		# со ссылкой на оплату
		order_items = OrderItemModel.objects.filter(order_id=request.session.get('order_created_id'))
		total_price = sum(item['quantity'] * item['price'] for item in order_items.values('price', 'quantity'))
		order = get_object_or_404(OrderModel, id=request.session.get('order_created_id'))
		return render(request, 'orders/created.html', {'order_items': order_items, 'total_price': total_price, 'order': order})
	cart = Cart(request)
	if len(cart) == 0:
		msg = 'Ваша заявка пуста. Добавьте в неё услугу(и) для возможности перейти к шагу 2.'
		messages.add_message(request, messages.INFO, msg)
		return redirect('orders:order_prepare')

	form = OrderForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			order = form.save()
			for item in cart:
				OrderItemModel.objects.create(
					order=order,
					product=item['product'],
					quantity=item['quantity'],
					price=item['price']
				)
			request.session['order_created_id'] = order.id
			cart.clear()
			return redirect('orders:order_create')
	return render(request, 'orders/create.html', {'form': form})


def order_reset(request):
	if request.session.get('order_created_id'):
		del request.session['order_created_id']
		request.session.modified = True
		messages.add_message(request, messages.SUCCESS, 'Ваша заявка была сброшена.')
	return redirect('orders:order_prepare')
