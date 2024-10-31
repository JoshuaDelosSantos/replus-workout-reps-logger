"""
Author: Joshua Delos Santos
Date: 29/10/2024
"""

from django import forms
from base.models import Session

class SessionForm(forms.ModelForm):
    """
    Form for creating a new session.
    """
    class Meta:
        model = Session
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': ' Ex. Push Day', 'class': 'session-form-control'}),
        }