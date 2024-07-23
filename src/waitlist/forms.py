from django import forms

from .models import WaitlistEntry


class WaitlistForm(forms.ModelForm):
    class Meta:
        model = WaitlistEntry
        fields = ["name", "email"]

    def clean(self):
        cleaned_data = super().clean()
        if self.errors.get("email"):
            # If there's an error with the email, remove it from cleaned_data
            cleaned_data.pop("email", None)
        return cleaned_data
