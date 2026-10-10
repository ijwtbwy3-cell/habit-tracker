from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import HabitLog


@receiver(post_save, sender = HabitLog)
def update_habit_after_log(sender, instance, created, **kwargs):
    if not created:
        return

    habit = instance.habit
    habit.last_completed_at = instance.created_at
    habit.update_streak()
    habit.save(update_fields = ['last_completed_at', 'current_streak'])
