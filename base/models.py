"""
Class Models

Author: Joshua Delos Santos
Date: 07/10/2024
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError 



MAX_CHAR_FIELD = 25
MAX_DIGITS = 5
NUMBER_DECIMAL_PLACE = 2



class Session(models.Model):
    """
    The Session model represents a user-specific session with a unique name and slug.
    
    Attributes:
        name (CharField): The name of the session, which must be unique.
        slug (SlugField): A unique slug for the session, automatically generated from the name.
        user (ForeignKey): A reference to the User who owns the session.
    """
    name = models.CharField(max_length=MAX_CHAR_FIELD, unique=True)  # Django will raise an IntegrityError when creating a duplicate.
    slug = models.SlugField(unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')  # Link to User
    
    
    def __str__(self):
        """
        Returns a string representation of the session.
        """
        return self.name
    
    
    def save(self, *args, **kwargs):
        """
        Override the save method to enforce uniqueness of the session name and 
        automatically set the slug based on the session name.
        """
        if Session.objects.filter(name__iexact=self.name, user=self.user).exists() and not self.pk:
            raise ValidationError(f"A similar session to '{self.name}' already exists.")
        
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)
            
        super().save(*args, **kwargs)
    


class Exercise(models.Model):
    """
    The Exercise model represents an exercise within a session, with a unique name and slug.
    
    Attributes:
        name (CharField): The name of the exercise.
        session (ForeignKey): A reference to the Session to which the exercise belongs.
        slug (SlugField): A unique slug for the exercise, automatically generated from the name.
        user (ForeignKey): A reference to the User who owns the exercise.
    """
    name = models.CharField(max_length=MAX_CHAR_FIELD)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='exercises', null=True)
    slug = models.SlugField(unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercises')
    
    
    def __str__(self):
        """
        Returns a string representation of the exercise.
        """
        return self.name
    
    
    def save(self, *args, **kwargs):
        """
        Override the save method to enforce uniqueness of the exercise name within a session
        and automatically set the slug based on the exercise name.
        """
        if Exercise.objects.filter(name__iexact=self.name, session=self.session, user=self.user).exists() and not self.pk:
            raise ValidationError(f"A similar exercise to '{self.name}' already exists.")
        
        # Automatically generate the slug from the name
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)
        
        super().save(*args, **kwargs)
    
    
    def determine_average_reps(self):
        """
        Determine the average number of reps for the exercise.
        """
        total_reps = sum(line.reps for line in self.lines.all())
        count = self.lines.count()
        return total_reps / count if count > 0 else 0
    
    
    
class Line(models.Model):
    """
    The Line model represents a single set of an exercise, with a weight, reps, date, and slug.
    
    Attributes:
        exercise (ForeignKey): A reference to the Exercise to which the line belongs.
        weight (DecimalField): The weight lifted for the set.
        reps (IntegerField): The number of repetitions performed for the set.
        date (DateTimeField): The date and time the set was performed.
        slug (SlugField): A unique slug for the line, automatically generated from the exercise name and date.
        user (ForeignKey): A reference to the User who owns the line.
    """
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='lines')
    weight = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=NUMBER_DECIMAL_PLACE)
    reps = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lines') 
    
    
    def __str__(self):
        """
        Returns a string representation of the line.
        """
        return f"{self.weight} for {self.reps} reps at {self.date}"
    
    
    def save(self, *args, **kwargs):
        """
        Override the save method to automatically set the slug based on the exercise name and date.
        """
        if not self.slug or self.slug != slugify(f"{self.exercise.name}-{self.date}"):
            self.slug = slugify(f"{self.exercise.name}-{self.date}")
        
        super().save(*args, **kwargs)