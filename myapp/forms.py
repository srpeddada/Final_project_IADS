from django import forms
from myapp.models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('client', 'product', 'num_units')
        client = forms.ChoiceField(widget=forms.RadioSelect)
        num_units = forms.IntegerField(label='Quantity')
        client = forms.CharField(label='Client Name')


class InterestForm(forms.Form):
    interested = forms.ChoiceField(widget=forms.RadioSelect, choices=[(1, "Yes"), (0, "No")])
    quantity = forms.IntegerField(min_value=1)
    comments = forms.CharField(widget=forms.Textarea, label='Additional Comments', required=False)