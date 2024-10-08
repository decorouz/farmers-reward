from django import forms
from phonenumber_field.formfields import PhoneNumberField

from .models import Contact

name_class = {
    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
}


class ContactUsForm(forms.ModelForm):
    phone_number = PhoneNumberField(
        widget=forms.TextInput(
            attrs={
                "class": name_class["class"],
                "placeholder": "Phone number",
            }
        ),
        required=False,
    )

    class Meta:
        model = Contact
        fields = ["name", "email", "phone_number", "message"]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": name_class["class"],
                    "placeholder": "Full Name",
                    "required": True,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": name_class["class"],
                    "placeholder": "E-mail",
                    "required": True,
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": name_class["class"],
                    "placeholder": "Message",
                    "cols": 50,
                    "rows": 7,
                }
            ),
        }
