from django import forms
from .models import Rating, Spot, Visitor

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['visitor', 'spot', 'score', 'comment']

class SpotForm(forms.ModelForm):
    class Meta:
        model = Spot
        # Adjust the fields as necessary per your model's definition
        fields = ['name', 'location', 'category']

class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ['name']

class AddRatingForm(forms.Form):
    visitor_name = forms.CharField(max_length=120, label="Your Name")
    visitor_age = forms.IntegerField(min_value=0, label="Your Age")
    spot = forms.ModelChoiceField(queryset=Spot.objects.all(), label="Select Spot")
    score = forms.IntegerField(min_value=1, max_value=5, label="Score")
    comment = forms.CharField(max_length=255, required=False, label="Comment")