"""
Author: Joshua Delos Santos
Date: 31/10/2024
"""

from django import forms
from base.models import Line

class LineForm(forms.ModelForm):
    """
    Form for creating a new line.
    """
    class Meta:
        model = Line
        fields = ['weight', 'reps']
        labels = {
            'weight': 'Weight',  # Custom label for the weight field
            'reps': 'Reps  ',  # Custom label for the reps field
        }
        widgets = {
            'weight': forms.TextInput(attrs={'class': 'weight-input'}),
            'reps': forms.TextInput(attrs={'class': 'reps-input'}),
        }
