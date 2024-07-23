import logging

from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import WaitlistForm

# Create your views here.

logger = logging.getLogger(__name__)


def join_waitlist(request):
    if request.method == "POST":
        form = WaitlistForm(request.POST)
        logger.info(f"Form data: {request.POST}")
        if form.is_valid():
            logger.info("Form is valid")
            try:

                instance = form.save()
                logger.info(f"Instance saved: {instance}")
                messages.success(request, "You have successfully joined the waitlist.")
                return redirect("waitlist_success")
            except Exception as e:
                logger.error(f"Error saving form: {str(e)}")
                messages.error(request, "An error occurred. Please try again.")
        else:
            logger.error(f"Form errors: {form.errors}")
    else:
        form = WaitlistForm()
    return render(request, "waitlist/join_waitlist_form.html", {"form": form})


def waitlist_success(request):
    return render(request, "waitlist/success.html")
