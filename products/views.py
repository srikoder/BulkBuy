from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from products import models as product_models
from accounts import models as accounts_models
from orders import models as orders_models
from django.views import generic
from braces.views import SelectRelatedMixin
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts import decorators
from django.utils.decorators import method_decorator
from products import forms
from django.contrib.auth import get_user_model
from django.http import Http404
# Create your views here.
User = get_user_model()

class ProductListView(generic.ListView, SelectRelatedMixin):
    model = product_models.Product
    paginate_by = 14
    select_related = ('vendor')

@method_decorator([decorators.vendor_required], name='dispatch')
class ProductCreateView(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    form_class = forms.ProductForm
    model = product_models.Product

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.vendor = accounts_models.Vendor.objects.get(user = self.request.user)
        self.object.save()
        return super().form_valid(form)


class ProductDetailView(generic.DetailView):
    model = product_models.Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        context['reviews'] = product_models.ProductReview.objects.filter(product__pk = context['view'].kwargs['pk'])
        return context
    

@method_decorator([decorators.vendor_required], name='dispatch')
class ProductUpdateView(generic.UpdateView, LoginRequiredMixin):
    form_class = forms.ProductForm
    model = product_models.Product

class ProductDeleteView(generic.DeleteView, LoginRequiredMixin):
    model = product_models.Product
    success_url = reverse_lazy('products:all')

    def dispatch(self, request, *args, **kwargs):
        product = product_models.Product.objects.get(pk = kwargs['pk'])
        product_orders = orders_models.Order.objects.filter(product = product)
        for order in product_orders:
            order.status = 'CL'
            order.save()
        return super().dispatch(request, *args, **kwargs)

class VendorProductListView(generic.ListView):
    model = product_models.Product
    template_name = "products/vendor_product_list.html"
    paginate_by = 6

    def get_queryset(self):
        try:
            user = accounts_models.User.objects.get(username = self.kwargs.get("username"))
            vendor = accounts_models.Vendor.objects.get(user = user)
            vendor_products = product_models.Product.objects.filter(vendor = vendor)
        except User.DoesNotExist:
            raise Http404
        else:
            return vendor_products

    def get_context_data(self, **kwargs):
        user = accounts_models.User.objects.get(username = self.kwargs.get("username"))
        vendor = accounts_models.Vendor.objects.get(user = user)
        context = super().get_context_data(**kwargs)
        context["product_vendor"] = vendor
        return context

class ProductSearchResultsView(generic.ListView):
    model = product_models.Product
    paginate_by = 6
    template_name = 'products/product_search.html'

    def get_queryset(self):
        result = super(ProductSearchResultsView, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            result = result.filter(name__icontains = query)
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_q'] = self.request.GET.get('q')
        return context


def dispatchProduct(request, pk):
    product = product_models.Product.objects.get(pk = pk)
    product_orders = orders_models.Order.objects.filter(product = product, status = 'PC')
    product.last_dispatch = product.number_of_orders_received
    for order in product_orders:
        order.status = 'DP'
        order.save()
    product.number_of_orders_received = 0
    product.save()
    return redirect('products:single', pk = pk)

def cancelDispatch(request, pk):
    product = product_models.Product.objects.get(pk = pk)
    product_orders = orders_models.Order.objects.filter(product = product, status = 'DP')
    product.number_of_orders_received += product.last_dispatch
    product.last_dispatch = 0
    for order in product_orders:
        order.status = 'CL'
        order.save()
    product.save()
    return redirect('products:single', pk = pk)
    
@method_decorator([decorators.customer_required], name='dispatch')
class ProductReviewCreateView(generic.CreateView, LoginRequiredMixin):
    form_class = forms.ProductReviewForm
    model = product_models.ProductReview

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = context['view'].kwargs['pk']
        return context
    

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.product = product_models.Product.objects.get(pk = self.kwargs['pk'])
        self.object.author = accounts_models.Customer.objects.get(user = self.request.user)
        if self.object.product.rating:
            self.object.product.rating = ((self.object.product.rating*self.object.product.number_of_reviews)+self.object.rating)/(self.object.product.number_of_reviews+1)
            self.object.product.number_of_reviews += 1
            self.object.product.save()
        else:
            self.object.product.rating = self.object.rating
            self.object.product.number_of_reviews += 1
            self.object.product.save()
        self.object.save()
        return super().form_valid(form)


class ProductReviewDetailView(generic.DetailView):
    model = product_models.ProductReview