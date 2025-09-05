# reviews/forms.py
from django import forms
from .models import Review

# Search form (manual)
class BookSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=True)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border rounded', 'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded', 'rows': 4}),
        }