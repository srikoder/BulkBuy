from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from accounts import views
from accounts.forms import CustomerLoginForm, VendorLoginForm
app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup/vendor/', views.VendorSignUpView.as_view(), name='vendor_signup'),
    path('signup/customer', views.CustomerSignUpView.as_view(), name='customer_signup'),

    path('login/', views.LoginView.as_view(), name='login'),
    path('login/customer_login', auth_views.LoginView.as_view(template_name='accounts/login/customer_login.html', authentication_form = CustomerLoginForm), name='customer_login'),
    path('login/vendor_login', auth_views.LoginView.as_view(template_name='accounts/login/vendor_login.html', authentication_form = VendorLoginForm), name='vendor_login'),

    re_path(r"logout/$", auth_views.LogoutView.as_view(), name="logout"),
]
