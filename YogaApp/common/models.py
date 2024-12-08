from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from YogaApp.accounts.models import Profile
from YogaApp.yoga_classes.models import YogaClass

UserModel = get_user_model()


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="bookings")
    yoga_class = models.ForeignKey(YogaClass, on_delete=models.CASCADE, related_name="bookings")
    booking_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def save(self, *args, **kwargs):
        total_bookings = self.yoga_class.bookings.exclude(pk=self.pk).count() + 1
        if total_bookings < 3:
            self.status = 'pending'
        elif 3 <= total_bookings < 20:
            self.status = 'confirmed'
        else:
            self.status = 'cancelled'
        super().save(*args, **kwargs)


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="reviews")
    yoga_class = models.ForeignKey(YogaClass, on_delete=models.CASCADE, related_name="reviews", null=True, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comments = models.TextField(max_length=500, blank=True, null=True)
    review_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


class Goal(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="goals")
    description = models.CharField(max_length=255)
    target_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description


