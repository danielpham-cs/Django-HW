from django.core.management.base import BaseCommand

from core.models import Rating, Spot, Visitor


class Command(BaseCommand):
    help = "Load a small set of sample data (idempotent)."

    def handle(self, *args, **options):
        if Visitor.objects.exists() or Spot.objects.exists():
            self.stdout.write("Data already present, skipping seed.")
            return

        alice = Visitor.objects.create(name="Alice", age=28)
        bob = Visitor.objects.create(name="Bob", age=35)
        carol = Visitor.objects.create(name="Carol", age=22)

        beach = Spot.objects.create(
            name="Sunset Beach", location="Da Nang", category="Beach"
        )
        temple = Spot.objects.create(
            name="Old Temple", location="Hue", category="Historic"
        )
        peak = Spot.objects.create(
            name="Fansipan Peak", location="Sapa", category="Mountain"
        )

        Rating.objects.create(visitor=alice, spot=beach, score=5, comment="Beautiful sunset!")
        Rating.objects.create(visitor=bob, spot=temple, score=4, comment="Very peaceful.")
        Rating.objects.create(visitor=carol, spot=peak, score=5, comment="Amazing view.")
        Rating.objects.create(visitor=alice, spot=peak, score=3, comment="Cold but nice.")

        self.stdout.write(self.style.SUCCESS("Sample data created."))
