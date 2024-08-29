from django import forms

from .models import Contact


class WaitlistForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email"]
