from django.contrib import messages
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RatingForm, SpotForm, VisitorForm
from .models import Rating, Spot, Visitor


def _spots_with_stats():
    return Spot.objects.annotate(
        avg_score=Avg("ratings__score"),
        rating_count=Count("ratings"),
    )


def home(request):
    """Landing page with destination filter and related content."""
    spots = _spots_with_stats()
    selected_spot_id = request.GET.get("spot")
    selected_spot = None
    if selected_spot_id:
        selected_spot = spots.filter(pk=selected_spot_id).first()

    ratings = Rating.objects.select_related("visitor", "spot")
    if selected_spot:
        ratings = ratings.filter(spot=selected_spot)

    popular_spots = spots.order_by("-avg_score", "-rating_count", "name")[:6]

    if selected_spot:
        recommended_spots = (
            spots.exclude(pk=selected_spot.pk)
            .filter(category=selected_spot.category)
            .order_by("-avg_score", "name")[:4]
        )
        if not recommended_spots:
            recommended_spots = spots.exclude(pk=selected_spot.pk).order_by("name")[:4]
    else:
        recommended_spots = popular_spots[:4]

    categories = (
        Spot.objects.order_by("category")
        .values_list("category", flat=True)
        .distinct()
    )

    context = {
        "spots": spots.order_by("name"),
        "selected_spot": selected_spot,
        "selected_spot_id": selected_spot_id,
        "popular_spots": popular_spots,
        "recommended_spots": recommended_spots,
        "categories": categories,
        "ratings": ratings[:9],
        "stats": {
            "spots": spots.count(),
            "ratings": Rating.objects.count(),
            "categories": len(categories),
        },
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
    # Restrict users to only view the list of visitors
    return render(request, "core/visitor_list.html", {"visitors": Visitor.objects.all()})


# Remove the ability for users to create new visitors


# Remove the ability for users to update visitors


# Remove the ability for users to delete visitors


# ------------------------------ Spots --------------------------------------
def spot_list(request):
    spots = Spot.objects.all()
    spot_id = request.GET.get("spot")
    category = request.GET.get("category")
    if spot_id:
        spots = spots.filter(pk=spot_id)
    if category:
        spots = spots.filter(category__iexact=category)
    return render(
        request,
        "core/spot_list.html",
        {
            "spots": spots,
            "selected_spot_id": spot_id,
            "selected_category": category,
        },
    )


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
    from .forms import AddRatingForm
    if request.method == "POST":
        form = AddRatingForm(request.POST)
        if form.is_valid():
            visitor_name = form.cleaned_data["visitor_name"]
            visitor_age = form.cleaned_data["visitor_age"]
            spot = form.cleaned_data["spot"]
            score = form.cleaned_data["score"]
            comment = form.cleaned_data["comment"]
            visitor, created = Visitor.objects.get_or_create(
                name=visitor_name,
                defaults={"age": visitor_age},
            )
            if not created and visitor.age != visitor_age:
                visitor.age = visitor_age
                visitor.save(update_fields=["age"])
            Rating.objects.create(visitor=visitor, spot=spot, score=score, comment=comment)
            return redirect("rating_list")
    else:
        form = AddRatingForm()
    return render(
        request,
        "core/form.html",
        {"form": form, "title": "Add Rating", "list_url": "rating_list"},
    )

def rating_update(request, pk):
    return _update(request, Rating, RatingForm, pk, "rating_list", "Rating")


def rating_delete(request, pk):
    return _delete(request, Rating, pk, "rating_list", "Rating")
