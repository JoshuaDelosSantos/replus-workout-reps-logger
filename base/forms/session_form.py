from django import forms
from base.models import Session

class SessionForm(forms.ModelForm):
    """
    Form for creating a new session.
    """
    class Meta:
        model = Session
        fields = ['name']