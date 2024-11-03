"""
Author: Joshua Delos Santos
Date: 28/10/2024
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from base.viewModels.sessions_view_model import SessionsViewModel

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
        
        # There are only two possible POST requests: 
        # Add a session or delete a session.
        if 'delete_session' in request.POST:
            self._handle_delete_session(request, view_model)
        else:
            self._handle_add_session(request, view_model)
        
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
        """
        form = view_model.get_session_form(request.POST)
        
        if form.is_valid():
            # Using form data, create a new session for user.
            session = view_model.create_session(form)
            try:
                session.save()
                return redirect('sessions')
            except Exception as e:
                form.add_error(None, e.message)