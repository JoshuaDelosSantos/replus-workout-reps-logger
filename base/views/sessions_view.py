"""
Author: Joshua Delos Santos
Date: 28/10/2024
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from base.viewModels.sessions_view_model import SessionsViewModel
from django.core.exceptions import ValidationError


class SessionsView(LoginRequiredMixin, View):
    """
    View to display and add sessions for the authenticated user.
    """
    def setup(self, request, *args, **kwargs):
        """
        Initialize view_model before dispatch.
        Called by Django for each request.
        """
        super().setup(request, *args, **kwargs)
        self.view_model = SessionsViewModel(request.user)
        
        
    def get(self, request):
        """
        Handle GET requests: display the list of sessions and the form to add a new session.
        """ 
        context = self._get_context()
        
        return render(request, 'base/sessions.html', context)
    
    
    def post(self, request):
        """
        Handle POST requests: process the form to add a new session or delete a session.
        """
        if 'delete_session' in request.POST:
            self._handle_delete_session(request)
        else:
            return self._handle_add_session(request)
        
        context = self._get_context()
        return render(request, 'base/sessions.html', context)


    def _handle_delete_session(self, request):
        """
        Handle the deletion of a session.
        """
        session_slug = request.POST.get('session_slug')
        self.view_model.delete_session(session_slug)
        return redirect('sessions')
    
    
    def _get_context(self):
        """
        Get the context for the view.
        """
        sessions = self.view_model.get_sessions()
        form = self.view_model.get_session_form()
        
        return {
            'sessions': sessions,
            'form': form
        }
    
    
    def _handle_add_session(self, request):
        """
        Handle adding a session.
        
        Return:
            - If the form is valid, redirect to the sessions page.
            - If the form is invalid, display the form with the errors. 
        """
        form = self.view_model.get_session_form(request.POST)
        
        if form.is_valid():
            try:
                # Using form data, create a new session for user.
                new_session = self.view_model.create_session(form)
                new_session.save()
                return redirect('sessions')
            except ValidationError as e:
                form.add_error('name', e)
        
        # If form is invalid, display the form with the errors.
        context = {
            'sessions': self.view_model.get_sessions(),
            'form': form
        }
        
        return render(request, 'base/sessions.html', context)
