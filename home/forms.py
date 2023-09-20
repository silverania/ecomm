from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['nome', 'cognome', 'email', 'via', 'postal', 'città']
