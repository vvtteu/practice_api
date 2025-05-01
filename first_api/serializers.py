from rest_framework import serializers
from .models import PerevalAdded, PerevalImages
from first_api.models import User

class PerevalImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalImages
        fields = '__all__'

class PerevalAddedSerializer(serializers.ModelSerializer):
    images = PerevalImagesSerializer(many=True)
    
    class Meta:
        model = PerevalAdded
        fields = '__all__'
        read_only_fields = ('status',)  
    def create(self, validated_data):
        images_data = validated_data.pop('images')
        pereval = PerevalAdded.objects.create(**validated_data)
        for image_data in images_data:
            PerevalImages.objects.create(pereval=pereval, **image_data)
        return pereval

class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для данных пользователя.
    
    """
    class Meta:
        model = User
        fields = ['email', 'phone', 'fam', 'name', 'otc']
        extra_kwargs = {
            'email': {
                'help_text': 'Обязательное поле. Email пользователя в формате example@domain.com',
                'required': True,
                'allow_blank': False,
            },
            'phone': {
                'help_text': 'Телефон в формате +7XXXXXXXXXX (минимум 11 цифр)',
                'required': True,
                'min_length': 11,
            },
            'fam': {
                'help_text': 'Фамилия пользователя (кириллица, латиница)',
                'required': True,
            },
            'name': {
                'help_text': 'Имя пользователя (кириллица, латиница)',
                'required': True,
            },
            'otc': {
                'help_text': 'Отчество пользователя (опционально)',
                'required': False,
                'allow_blank': True,
            }
        }