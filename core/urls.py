from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # Users (Visitor table)
    path("users/", views.visitor_list, name="visitor_list"),
    path("users/add/", views.visitor_create, name="visitor_create"),
    path("users/<int:pk>/edit/", views.visitor_update, name="visitor_update"),
    path("users/<int:pk>/delete/", views.visitor_delete, name="visitor_delete"),
    # Tourist attractions (Spot table)
    path("spots/", views.spot_list, name="spot_list"),
    path("spots/add/", views.spot_create, name="spot_create"),
    path("spots/<int:pk>/edit/", views.spot_update, name="spot_update"),
    path("spots/<int:pk>/delete/", views.spot_delete, name="spot_delete"),
    # Ratings
    path("ratings/", views.rating_list, name="rating_list"),
    path("ratings/add/", views.rating_create, name="rating_create"),
    path("ratings/<int:pk>/edit/", views.rating_update, name="rating_update"),
    path("ratings/<int:pk>/delete/", views.rating_delete, name="rating_delete"),
]
