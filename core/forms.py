from django import forms

from .models import Rating, Spot, Visitor


class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ["name", "age"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "input", "placeholder": "Full name"}),
            "age": forms.NumberInput(attrs={"class": "input", "min": 0}),
        }


class SpotForm(forms.ModelForm):
    class Meta:
        model = Spot
        fields = ["name", "location", "category"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "input", "placeholder": "Attraction name"}),
            "location": forms.TextInput(attrs={"class": "input", "placeholder": "City / Address"}),
            "category": forms.TextInput(attrs={"class": "input", "placeholder": "Beach, Mountain, Museum..."}),
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["visitor", "spot", "score", "comment"]
        widgets = {
            "visitor": forms.Select(attrs={"class": "input"}),
            "spot": forms.Select(attrs={"class": "input"}),
            "score": forms.NumberInput(attrs={"class": "input", "min": 1, "max": 5}),
            "comment": forms.TextInput(attrs={"class": "input", "placeholder": "Optional comment"}),
        }

    def clean_score(self):
        score = self.cleaned_data["score"]
        if not 1 <= score <= 5:
            raise forms.ValidationError("Score must be between 1 and 5.")
        return score
