from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils import timezone
# Create your models here.

class User(AbstractUser):
    is_vendor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=3)

    def __str__(self):
        return self.user.username


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class VendorReviews(models.Model):
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)
    author = models.ForeignKey('accounts.Customer', on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=500)

    def __str__(self):
        return self.text
