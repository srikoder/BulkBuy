from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect
from accounts import forms
from django.contrib.auth import login
# Create your views here.


class SignUpView(generic.TemplateView):
    template_name = 'accounts/signup.html'

class VendorSignUpView(generic.CreateView):
    form_class = forms.VendorSignUpForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/signup/vendor_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'vendor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('accounts:vendor_login')

class CustomerSignUpView(generic.CreateView):
    form_class = forms.CustomerSignUpForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/signup/customer_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('accounts:customer_login')

class LoginView(generic.TemplateView):
    template_name = 'accounts/login.html'
