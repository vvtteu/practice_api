from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import PerevalAdded
from .serializers import *

class PerevalViewSet(viewsets.ModelViewSet):
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalAddedSerializer

    def create(self, request, *args, **kwargs):
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