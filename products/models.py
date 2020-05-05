from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'product_images/user_{0}/{1}'.format(instance.vendor.id, filename)

class Product(models.Model):
    vendor = models.ForeignKey('accounts.Vendor', on_delete= models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to=user_directory_path, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    rating = models.FloatField(blank=True, null=True)
    number_of_reviews = models.PositiveIntegerField(default=0)
    number_of_orders_required = models.PositiveIntegerField(default=1)
    number_of_orders_received = models.PositiveIntegerField(default=0)
    last_dispatch = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "products:single", kwargs={'pk': self.pk}
        )

    def get_place_order_url(self):
        return reverse("orders:create", kwargs={
            'pk': self.pk
        })

    class Meta:
        ordering = ['-rating']

class ProductReview(models.Model):
    RATING_CHOICES = [
        (1, 'BAD'),
        (2, 'AVERAGE'),
        (3, 'GOOD'),
        (4, 'VERY GOOD'),
        (5, 'EXCELLENT')
    ]

    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    author = models.ForeignKey('accounts.Customer', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=500)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=3)

    def get_absolute_url(self):
        return reverse(
            "products:single_review", kwargs={'pk': self.pk}
        )

    def __str__(self):
        return self.text

    