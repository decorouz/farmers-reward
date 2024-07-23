from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import WaitlistForm

# Create your views here.


def join_waitlist(request):
    if request.method == "POST":
        form = WaitlistForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully joined the waitlist.")
            return redirect("waitlist_success")

    else:
        form = WaitlistForm()
    return render(request, "waitlist/join_waitlist_form.html", {"form": form})


def waitlist_success(request):
    return render(request, "waitlist/success.html")
