from django.shortcuts import render
from django.views import generic
from orders import models as orders_models
from accounts import models as accounts_models
from products import models as products_models
from braces.views import SelectRelatedMixin
from django.http import Http404
from accounts.decorators import customer_required, vendor_required
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from orders import forms
# Create your views here.

@method_decorator([customer_required], name='dispatch')
class CustomerOrdersView(generic.ListView, SelectRelatedMixin, LoginRequiredMixin):
    model = orders_models.Order
    select_related = ('product', 'customer')
    template_name = 'orders/order_list.html'

    def get_queryset(self):
        user = self.request.user
        customer = accounts_models.Customer.objects.get(user = user)
        try:
            result = orders_models.Order.objects.prefetch_related('product', 'customer').filter(customer = customer)
        except customer.DoesNotExist:
            raise Http404
        else:
            return result

@method_decorator([customer_required], name='dispatch')
class CreateOrderView(generic.CreateView, LoginRequiredMixin):
    form_class = forms.OrdersForm
    success_url = reverse_lazy('orders:customer_orders')        
    template_name = 'orders/order_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs['pk']
        self.user = request.user
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = products_models.Product.objects.get(pk = context['view'].kwargs['pk'])
        return context 

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.product = products_models.Product.objects.get(pk = self.pk)
        self.object.product.number_of_orders_received += self.object.quantity
        if self.object.product.number_of_orders_received > self.object.product.number_of_orders_required:
            self.object.status = 'PC'
            product_orders = orders_models.Order.objects.filter(product = self.object.product, status = 'WT')
            for order in product_orders:
                order.status = 'PC'
                order.save()
        self.object.product.save()
        self.object.customer = accounts_models.Customer.objects.get(user = self.user)
        self.object.save()
        return super().form_valid(form)