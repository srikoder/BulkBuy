from django import forms
from orders import models

class OrdersForm(forms.ModelForm):

    class Meta:
        fields = ('quantity',)
        model = models.Order
