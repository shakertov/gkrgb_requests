from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from catalog.models import ProductModel
from cart.cart import Cart
from cart.forms import CartAddProductForm
from django.contrib import messages


@require_POST
def cart_add(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(ProductModel, id=product_id)
	form = CartAddProductForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		cart.add(product, 1, cd['update'])
		messages.add_message(request, messages.SUCCESS, 'Услуга добавлена в заявку')
	return redirect('orders:order_prepare')


def cart_remove(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(ProductModel, id=product_id)
	cart.remove(product)
	messages.add_message(request, messages.SUCCESS, 'Услуга(и) удалена из заявки')
	return redirect('orders:order_prepare')
