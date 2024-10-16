"""
Class Models

Author: Joshua Delos Santos
Date: 07/10/2024
"""

from django.db import models

MAX_CHAR_FIELD = 50
MAX_DIGITS = 5
NUMBER_DECIMAL_PLACE = 2

class Session(models.Model):
    name = models.CharField(max_length=MAX_CHAR_FIELD, unique=True)  # Django will raise an IntegrityError when creating a duplicate.
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """
        Override the save method to enforce uniqueness of the session name.
        
        If a session with the same name already exists in the database and 
        this is a new instance (self.pk is None), raise a ValidationError.
        This prevents duplicate session names from being saved.
        """
        if Session.objects.filter(name=self.name).exists() and not self.pk:
            raise ValidationError(f"A session with the name '{self.name}' already exists.")
        super().save(*args, **kwargs)
    

class Exercise(models.Model):
    name = models.CharField(max_length=MAX_CHAR_FIELD)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='exercises', null=True)
    
    def __str__(self):
        return self.name
    
    def determine_average_reps(self):
        total_reps = sum(line.reps for line in self.lines.all())
        count = self.lines.count()
        return total_reps / count if count > 0 else 0
    
class Line(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='lines')
    weight = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=NUMBER_DECIMAL_PLACE)
    reps = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.weight} for {self.reps} reps at {self.date}"