from django.db import models
from YogaApp.accounts.models import Profile


class Instructor(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)
    specializations = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - Instructor"


class YogaClass(models.Model):
    LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    STUDIO_CHOICES = (
        ('earth', 'Earth'),
        ('air', 'Air'),
    )

    name = models.CharField(max_length=100)
    schedule = models.DateTimeField()
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, related_name="classes")
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES)
    description = models.TextField(max_length=500)
    studio = models.CharField(choices=STUDIO_CHOICES, default=None)

    def __str__(self):
        return f"{self.name} - {self.get_level_display()} ({self.studio})"







