from django.urls import path

from .views import (
    CategoryListCreateAPIView,
    HabitCreateAPIView,
    HabitDetailAPIView,
    HabitDoneAPIView,
    HabitListAPIView,
    LoginAPIView,
    LogoutAPIView,
)

urlpatterns = [
    path('api/login/', LoginAPIView.as_view()),
    path('api/logout/', LogoutAPIView.as_view()),
    path('api/categories/', CategoryListCreateAPIView.as_view()),
    path('api/habits/', HabitListAPIView.as_view()),
    path('api/habit/new/', HabitCreateAPIView.as_view()),
    path('api/habit/<int:pk>/', HabitDetailAPIView.as_view()),
    path('api/habit/<int:pk>/done/', HabitDoneAPIView.as_view()),

    path('', HabitListAPIView.as_view()),
    path('habit/new/', HabitCreateAPIView.as_view()),
    path('habit/<int:pk>/', HabitDetailAPIView.as_view()),
    path('habit/<int:pk>/done/', HabitDoneAPIView.as_view()),
]
