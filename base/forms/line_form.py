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
            'weight': '',
            'reps': '',  
        }
        widgets = {
            'weight': forms.TextInput(attrs={'class': 'weight-input', 'placeholder': ' Weight'}),
            'reps': forms.TextInput(attrs={'class': 'reps-input', 'placeholder': '  Reps'}),
        }
