"""
Author: Joshua Delos Santos
Date: 31/10/2024
"""

from django import forms
from base.models import Exercise

class ExerciseForm(forms.ModelForm):
    """
    A form for creating and updating Exercise instances.
    """

    class Meta:
        model = Exercise
        fields = ['name']