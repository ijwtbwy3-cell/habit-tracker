from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'categories')
    name = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'habits')
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = 'habits')
    name = models.CharField(max_length = 200)
    description = models.TextField(blank = True)
    goal_per_week = models.PositiveIntegerField(default = 3)
    is_active = models.BooleanField(default = True)
    current_streak = models.PositiveIntegerField(default = 0)
    last_completed_at = models.DateTimeField(null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def update_streak(self):
        dates = []
        for log in self.logs.all():
            dates.append(log.date)

        cursor = timezone.localdate()
        if cursor not in dates:
            cursor -= timedelta(days = 1)

        streak = 0
        while cursor in dates:
            streak += 1
            cursor -= timedelta(days = 1)
        self.current_streak = streak


class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete = models.CASCADE, related_name = 'logs')
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.habit.name} — {self.date}'

    def clean(self):
        if self.date and self.date > timezone.localdate():
            raise ValidationError({'date': 'нельзя отмечать будущую дату.'})
        if self.habit_id and HabitLog.objects.filter(
            habit = self.habit,
            date = self.date,
        ).exclude(pk = self.pk).exists():
            raise ValidationError({'date': 'эта привычка уже отмечена на этот день.'})

