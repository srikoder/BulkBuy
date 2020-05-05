from django.db import models
from accounts import models as accounts_models
from products import models as products_models
from django.urls import reverse

# Create your models here.
class Order(models.Model):

    STATUS_CHOICES = [
        ('WT', 'WAITING'),
        ('PC', 'PLACED'),
        ('DP','DISPATCHED'),
        ('CL', 'CANCELLED')
    ]

    product = models.ForeignKey(products_models.Product, blank=True, null=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey(accounts_models.Customer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(choices = STATUS_CHOICES, max_length=2, default='WT')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.quantity) + ' of ' + self.product.name + ' by ' + self.product.vendor.user.username + ' ordered by ' + self.customer.user.username


    class Meta:
        ordering = ['-created_at']