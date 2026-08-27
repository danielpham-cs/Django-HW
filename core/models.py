from django.db import models


class Visitor(models.Model):
    """The 'User' table: people who rate tourist attractions.

    Named ``Visitor`` internally so it does not collide with Django's
    built-in ``auth.User``. It is shown as "User" in the UI.
    """

    name = models.CharField(max_length=120)
    age = models.PositiveIntegerField()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Spot(models.Model):
    """The 'Tourist attraction' table."""

    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    category = models.CharField(
        max_length=120,
        help_text="Area / Category, e.g. Beach, Mountain, Museum",
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Rating(models.Model):
    """The 'Rating' table: a visitor's score for a spot."""

    visitor = models.ForeignKey(
        Visitor, on_delete=models.CASCADE, related_name="ratings"
    )
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE, related_name="ratings")
    score = models.PositiveSmallIntegerField(help_text="1 to 5")
    comment = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.visitor} → {self.spot}: {self.score}"
