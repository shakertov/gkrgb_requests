from django.urls import path
from cart import views as v


app_name = 'cart'

urlpatterns = [
    path('add/<int:product_id>/', v.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', v.cart_remove, name='cart_remove'),
]
