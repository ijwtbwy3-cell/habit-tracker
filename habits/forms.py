from django import forms

from .models import Habit, HabitLog


class HabitForm(forms.ModelForm):
    goal_per_week = forms.IntegerField(
        min_value = 1,
        error_messages = {'min_value': 'цель должна быть больше нуля.'},
    )

    class Meta:
        model = Habit
        fields = ['category', 'name', 'description', 'goal_per_week', 'is_active']
        labels = {
            'category': 'категория',
            'name': 'название',
            'description': 'описание',
            'goal_per_week': 'цель в неделю',
            'is_active': 'активна',
        }



class HabitLogForm(forms.ModelForm):
    class Meta:
        model = HabitLog
        fields = ['date']
        labels = {'date': 'дата'}