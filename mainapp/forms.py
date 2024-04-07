#CHANGED ----------- CHANGED ----------- CHANGED
# forms.py

from django import forms

class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=100)
    address = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()
    # Add more fields as needed

class PaymentForm(forms.Form):
    credit_card_number = forms.CharField(max_length=16)
    expiration_date = forms.CharField(max_length=5)
    cvv = forms.CharField(max_length=3)
    billing_address = forms.CharField(widget=forms.Textarea)
    # Add more fields as needed

class RatingForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5)
    # Add more fields as needed
