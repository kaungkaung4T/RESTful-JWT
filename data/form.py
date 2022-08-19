from django import forms
from data.models import Item


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control mb-2"}),
            "description": forms.Textarea(attrs={"class": "form-control mb-2"}),
            "price": forms.NumberInput(attrs={"class": "form-control mb-3"}),
        }
        fields = ["name", "description", "price"]
