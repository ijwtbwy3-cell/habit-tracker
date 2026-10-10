from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, serializers, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import HabitForm, HabitLogForm
from .models import Category, Habit


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username = username, password = password)

        if user is None:
            return Response({'error': 'неверный логин или пароль'}, status = status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        return Response({'message': 'вход выполнен успешно', 'user': user.username})


class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'выход выполнен'})


class CategoryListCreateAPIView(APIView):
    def get(self, request):
        categories = Category.objects.filter(user = request.user).order_by('name')
        data = [
            {
                'id': category.id,
                'name': category.name,
            }
            for category in categories
        ]
        return Response({'categories': data})

    def post(self, request):
        name = request.data.get('name')
        if not name or not name.strip():
            return Response({'error': 'нужно указать название категории'}, status = status.HTTP_400_BAD_REQUEST)

        category = Category.objects.create(user = request.user, name = name.strip())
        return Response({
            'message': 'категория создана',
            'category': {
                'id': category.id,
                'name': category.name,
            },
        }, status = status.HTTP_201_CREATED)


class HabitPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class HabitListAPIView(APIView):
    def get(self, request):
        habits = Habit.objects.filter(user = request.user)
        category_id = request.query_params.get('category')
        if category_id:
            habits = habits.filter(category_id = category_id)

        paginator = HabitPagination()
        page = paginator.paginate_queryset(habits.order_by('-created_at'), request)
        data = [
            {
                'id': habit.id,
                'name': habit.name,
                'category': habit.category.name,
                'goal_per_week': habit.goal_per_week,
                'current_streak': habit.current_streak,
                'is_active': habit.is_active,
            }
            for habit in page
        ]
        return paginator.get_paginated_response(data)


class HabitCreateAPIView(APIView):
    def post(self, request):
        form = HabitForm(request.data)
        if not form.is_valid():
            return Response({'errors': form.errors}, status = status.HTTP_400_BAD_REQUEST)
        if form.cleaned_data['category'].user != request.user:
            return Response({'errors': {'category': ['выберите свою категорию.']}}, status = status.HTTP_400_BAD_REQUEST)

        habit = form.save(commit = False)
        habit.user = request.user
        habit.save()
        return Response({
            'message': 'привычка создана',
            'habit': {
                'id': habit.id,
                'name': habit.name,
                'category': habit.category_id,
            },
        }, status = status.HTTP_201_CREATED)


class HabitDetailAPIView(APIView):
    def get(self, request, pk):
        habit = get_object_or_404(Habit, pk = pk, user = request.user)
        return Response({
            'id': habit.id,
            'name': habit.name,
            'description': habit.description,
            'category': habit.category_id,
            'goal_per_week': habit.goal_per_week,
            'current_streak': habit.current_streak,
        })

    def put(self, request, pk):
        habit = get_object_or_404(Habit, pk = pk, user = request.user)
        form = HabitForm(request.data, instance = habit)
        if not form.is_valid():
            return Response({'errors': form.errors}, status = status.HTTP_400_BAD_REQUEST)
        if form.cleaned_data['category'].user != request.user:
            return Response({'errors': {'category': ['выберите свою категорию.']}}, status = status.HTTP_400_BAD_REQUEST)

        form.save()
        return Response({'message': 'привычка обновлена'})

    def delete(self, request, pk):
        habit = get_object_or_404(Habit, pk = pk, user = request.user)
        habit.delete()
        return Response({'message': 'привычка удалена'})


class HabitDoneAPIView(APIView):
    def post(self, request, pk):
        habit = get_object_or_404(Habit, pk = pk, user = request.user)
        form = HabitLogForm(data = {'date': timezone.localdate()})
        form.instance.habit = habit
        if not form.is_valid():
            return Response({'errors': form.errors}, status = status.HTTP_400_BAD_REQUEST)

        form.save()

        return Response({'message': 'привычка отмечена выполненной'})
