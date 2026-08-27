from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RatingForm, SpotForm, VisitorForm
from .models import Rating, Spot, Visitor


def home(request):
    """Landing page showing all three tables at a glance."""
    context = {
        "visitors": Visitor.objects.all(),
        "spots": Spot.objects.all(),
        "ratings": Rating.objects.select_related("visitor", "spot").all(),
    }
    return render(request, "core/home.html", context)


# ---------------------------------------------------------------------------
# Generic helpers: every model reuses the same create/update/delete flow.
# GET  -> render a form (create/update) or the list (delete confirmation).
# POST -> perform the write action, then redirect back to the list.
# ---------------------------------------------------------------------------
def _create(request, form_class, list_url, title):
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"{title} created successfully.")
            return redirect(list_url)
    else:
        form = form_class()
    return render(
        request,
        "core/form.html",
        {"form": form, "title": f"Add {title}", "list_url": list_url},
    )


def _update(request, model, form_class, pk, list_url, title):
    obj = get_object_or_404(model, pk=pk)
    if request.method == "POST":
        form = form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"{title} updated successfully.")
            return redirect(list_url)
    else:
        form = form_class(instance=obj)
    return render(
        request,
        "core/form.html",
        {"form": form, "title": f"Edit {title}", "list_url": list_url},
    )


def _delete(request, model, pk, list_url, title):
    obj = get_object_or_404(model, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, f"{title} deleted.")
        return redirect(list_url)
    # GET -> show a confirmation page
    return render(
        request,
        "core/confirm_delete.html",
        {"object": obj, "title": title, "list_url": list_url},
    )


# ------------------------------ Visitors (User) ----------------------------
def visitor_list(request):
    return render(request, "core/visitor_list.html", {"visitors": Visitor.objects.all()})


def visitor_create(request):
    return _create(request, VisitorForm, "visitor_list", "User")


def visitor_update(request, pk):
    return _update(request, Visitor, VisitorForm, pk, "visitor_list", "User")


def visitor_delete(request, pk):
    return _delete(request, Visitor, pk, "visitor_list", "User")


# ------------------------------ Spots --------------------------------------
def spot_list(request):
    return render(request, "core/spot_list.html", {"spots": Spot.objects.all()})


def spot_create(request):
    return _create(request, SpotForm, "spot_list", "Tourist Attraction")


def spot_update(request, pk):
    return _update(request, Spot, SpotForm, pk, "spot_list", "Tourist Attraction")


def spot_delete(request, pk):
    return _delete(request, Spot, pk, "spot_list", "Tourist Attraction")


# ------------------------------ Ratings ------------------------------------
def rating_list(request):
    ratings = Rating.objects.select_related("visitor", "spot").all()
    return render(request, "core/rating_list.html", {"ratings": ratings})


def rating_create(request):
    return _create(request, RatingForm, "rating_list", "Rating")


def rating_update(request, pk):
    return _update(request, Rating, RatingForm, pk, "rating_list", "Rating")


def rating_delete(request, pk):
    return _delete(request, Rating, pk, "rating_list", "Rating")
