from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import PerevalAdded, User, PerevalImages
from .serializers import *
"""
    API для работы с перевалами.
    
    list:
    Возвращает список всех перевалов (можно фильтровать по email пользователя через ?user__email=...).
    
    retrieve:
    Возвращает детали перевала по ID.
    
    create:
    Создает новый перевал. Требуется поле 'user' с данными пользователя.
    
    update:
    Обновляет данные перевала (только если статус 'new').
    
    moderate:
    Изменяет статус модерации перевала.
    
    """
class PerevalViewSet(viewsets.ModelViewSet):
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalAddedSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user_email = self.request.query_params.get('user__email', None)
        if user_email:
            if not User.objects.filter(email=user_email).exists():
                return queryset.none() 
            queryset = queryset.filter(user__email=user_email)
        return queryset

    def create(self, request, *args, **kwargs):
        if 'user' not in request.data:
            return Response(
                {'status': 'error', 'message': 'Поле "user" обязательно'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_data = request.data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        
        request.data['user'] = user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pereval = serializer.save(status='new')
        
        return Response(
            {'status': status.HTTP_201_CREATED, 'id': pereval.id},
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.status != 'new':
            return Response(
                {'state': 0, 'message': 'Редактирование запрещено: запись не в статусе "new"'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if 'user' in request.data:
            return Response(
                {'state': 0, 'message': 'Редактирование данных пользователя запрещено'},
                status=status.HTTP_400_BAD_REQUEST
            )

        images_data = request.data.pop('images', None)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        pereval = serializer.save()
        
        if images_data:
            pereval.images.all().delete()
            for image_data in images_data:
                PerevalImages.objects.create(pereval=pereval, **image_data)
        
        return Response({'state': 1})

    @action(detail=True, methods=['patch'])
    def moderate(self, request, pk=None):
        pereval = self.get_object()
        new_status = request.data.get('status')
        comment = request.data.get('moderator_comment', None)
        
        if new_status not in dict(PerevalAdded.STATUS_CHOICES).keys():
            return Response(
                {'status': 'error', 'message': 'Недопустимый статус'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        pereval.status = new_status
        pereval.moderator_comment = comment
        pereval.moderation_date = timezone.now()
        pereval.save()
        
        return Response(
            {'status': 'success', 'state': pereval.get_status_display()}
        )