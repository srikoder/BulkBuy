from django import forms
from products import models

class ProductForm(forms.ModelForm):

    class Meta:
        fields = ('name', 'description', 'image', 'price', 'number_of_orders_required')
        model = models.Product

class ProductReviewForm(forms.ModelForm):

    class Meta:
        fields = ('title', 'text', 'rating')
        model = models.ProductReview