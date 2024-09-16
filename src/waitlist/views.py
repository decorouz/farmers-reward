import time

from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ContactUsForm

# Create your views here.


def contact_us(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("contact_thanks")

    else:
        form = ContactUsForm()
    return render(request, "contact_us/contact_us_form.html", {"form": form})


# Send send confirmation email with pitch deck or summary
# Ensure only valid emails are accepted
# Ad htmx to handle form input and redirect.
