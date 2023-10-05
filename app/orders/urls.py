from django.urls import path
from orders import views as v


app_name = 'orders'

urlpatterns = [
    path('', v.order_prepare, name='order_prepare'),
    path('create/', v.order_create, name='order_create'),
    path('reset/', v.order_reset, name='order_reset'),
]
