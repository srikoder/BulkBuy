from django.urls import path, re_path
from orders import views

app_name = 'orders'

urlpatterns = [
    re_path('place/(?P<pk>\d+)', views.CreateOrderView.as_view(), name='create'),
    re_path('user/$', views.CustomerOrdersView.as_view(), name='customer_orders'),
]
