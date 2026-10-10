from django.contrib import admin

from .models import Category, Habit, HabitLog


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('user',)
    search_fields = ('name',)


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'category', 'goal_per_week', 'is_active', 'current_streak', 'last_completed_at')
    list_filter = ('user', 'category', 'is_active')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)


@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ('habit', 'date', 'created_at')
    list_filter = ('habit__user', 'date')
    search_fields = ('habit__name',)
