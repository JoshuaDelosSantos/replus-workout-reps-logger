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
    def get(self, request):
        """
        Handle GET requests: display the list of sessions and the form to add a new session.
        """
        view_model = SessionsViewModel(request.user)    
        context = self._get_context(view_model)
        
        return render(request, 'base/sessions.html', context)
    
    
    def post(self, request):
        """
        Handle POST requests: process the form to add a new session or delete a session.
        """
        view_model = SessionsViewModel(request.user)
        
        if 'delete_session' in request.POST:
            self._handle_delete_session(request, view_model)
        else:
            return self._handle_add_session(request, view_model)
        
        context = self._get_context(view_model)
        return render(request, 'base/sessions.html', context)


    def _handle_delete_session(self, request, view_model):
        """
        Handle the deletion of a session.
        """
        session_slug = request.POST.get('session_slug')
        view_model.delete_session(session_slug)
        return redirect('sessions')
    
    
    def _get_context(self, view_model):
        """
        Get the context for the view.
        """
        sessions = view_model.get_sessions()
        form = view_model.get_session_form()
        
        return {
            'sessions': sessions,
            'form': form
        }
    
    
    def _handle_add_session(self, request, view_model):
        """
        Handle adding a session.
        
        Return:
            - If the form is valid, redirect to the sessions page.
            - If the form is invalid, display the form with the errors. 
        """
        form = view_model.get_session_form(request.POST)
        
        if form.is_valid():
            try:
                # Using form data, create a new session for user.
                session = view_model.create_session(form)
                session.save()
                return redirect('sessions')
            except ValidationError as e:
                form.add_error('name', e)
        
        # If form is invalid, display the form with the errors.
        context = {
            'sessions': view_model.get_sessions(),
            'form': form
        }
        
        return render(request, 'base/sessions.html', context)
