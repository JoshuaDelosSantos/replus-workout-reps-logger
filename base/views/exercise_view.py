from django.shortcuts import render, get_object_or_404
from django.views import View
from base.models import Exercise, Session
from users.api.user_data import UserData
from base.forms.exercise_form import ExerciseForm

class ExerciseView(View):
    """
    A class-based view for displaying details of an Exercise.
    """

    def get(self, request, session_slug):
        """
        Handle GET requests to display the details of exercises in a session.
        """
        user_data = UserData(request.user)
        exercises = user_data.get_exercises_by_session_slug(session_slug)
        form = ExerciseForm()
        
        context = {
            'exercises': exercises, 
            'form': form
        }
        
        return render(request, 'base/exercise.html', context)
    
    def post(self, request, session_slug):
        """
        Handle POST requests to process the form to add a new exercise.
        """
        user_data = UserData(request.user)
        session = get_object_or_404(Session, slug=session_slug, user=request.user)
        form = ExerciseForm(request.POST)
        
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.user = request.user 
            exercise.session = session 
            try:
                exercise.save()
                return redirect('exercise', session_slug=session.slug)
            except ValidationError as e:
                form.add_error(None, e)
                
        context = {
            'session': session, 
            'exercises': exercises, 
            'form': form
            }
        
        exercises = user_data.get_exercises_by_session_slug(session_slug)
        return render(request, 'base/exercise.html', context)