"""
Author: Joshua Delos Santos
Date: 28/10/2024
"""

from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.views import View
from base.models import Session
from base.forms.session_form import SessionForm
from users.api.user_data import UserData

class SessionsView(LoginRequiredMixin, View):
    """
    View to display and add sessions for the authenticated user.
    """
    def get(self, request):
        """
        Handle GET requests: display the list of sessions and the form to add a new session.
        """
        user = UserData(request.user)
        sessions = user.get_user_sessions()
        form = SessionForm()
        
        context = {
            'sessions': sessions,
            'form': form
        }
        
        return render(request, 'base/sessions.html', context)
    
    def post(self, request):
        """
        Handle POST requests: process the form to add a new session.
        """
        user = request.user
        form = SessionForm(request.POST)
        
        if form.is_valid():
            session = form.save(commit=False)
            session.user = user
            try:
                session.save()
                return redirect('sessions_view')
            except ValidationError as e:
                form.add_error(None, e)
        
        sessions = Session.objects.filter(user=user)
        context = {
            'sessions': sessions,
            'form': form
        }
        
        return render(request, 'base/sessions.html', context)