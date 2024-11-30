from celery import shared_task


@shared_task
def delete_old_yoga_classes():
    from datetime import timedelta
    from django.utils.timezone import now
    from YogaApp.yoga_classes.models import YogaClass

    one_month_ago = now() - timedelta(days=30)
    old_classes = YogaClass.objects.filter(schedule__lt=one_month_ago)
    count = old_classes.count()
    old_classes.delete()
    return f'Deleted {count} old bookings'
