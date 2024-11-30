from django.contrib import admin
from .models import Booking, Review


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'yoga_class', 'status', 'booking_date')
    list_filter = ('status',)
    search_fields = ('yoga_class__name', 'yoga_class__level')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'review_date', 'comments')
    list_filter = ('rating',)
    search_fields = ('comments',)
