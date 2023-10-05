from django import forms
from orders.models import OrderModel


class OrderForm(forms.ModelForm):
	class Meta:
		model = OrderModel
		fields = ['first_name', 'last_name', 'email', 'city', 'address', 'comment']
