from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts import models
from django import forms
from django.db import transaction

class VendorSignUpForm(UserCreationForm):

    class Meta:
        model = models.User
        fields = ("username", "email", "password1", "password2")

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_vendor = True
        user.save()
        vendor = models.Vendor.objects.create(user = user)
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Display name"
        self.fields["email"].label = "Email address"


class CustomerSignUpForm(UserCreationForm):

    class Meta:
        model = models.User
        fields = ("username", "email", "password1", "password2")

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        vendor = models.Customer.objects.create(user = user)
        return user


class CustomerLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError('Inactive User', code='inactive')
        if user.is_vendor:
            raise forms.ValidationError('User type mismatch', code='type_mismatch')

class VendorLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError('Inactive User', code='inactive')
        if user.is_customer:
            raise forms.ValidationError('User type mismatch', code='type_mismatch')
