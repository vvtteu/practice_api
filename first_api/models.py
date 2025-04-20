from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class User(models.Model):
    """Модель пользователя (вынесена из JSON)"""
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    fam = models.CharField(max_length=100, verbose_name="Фамилия")
    name = models.CharField(max_length=100, verbose_name="Имя")
    otc = models.CharField(max_length=100, verbose_name="Отчество", blank=True)

    def __str__(self):
        return f"{self.fam} {self.name}"

class PerevalAreas(models.Model):
    """Географические области"""
    id_parent = models.BigIntegerField()
    title = models.TextField()

    class Meta:
        db_table = 'pereval_areas'

    def __str__(self):
        return self.title

class PerevalImages(models.Model):
    """Изображения перевалов"""
    date_added = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(upload_to='pereval_images/')
    title = models.CharField(max_length=255, blank=True)  
    class Meta:
        db_table = 'pereval_images'

    def __str__(self):
        return f"Image {self.id} - {self.title}"

class PerevalAdded(models.Model):
    """Информация о перевалах"""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    beauty_title = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255, blank=True)
    connect = models.TextField(blank=True)
    
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField(
        default=0,  
        null=True, 
        blank=True
    )
    
    level_winter = models.CharField(max_length=10, blank=True)
    level_summer = models.CharField(max_length=10, blank=True)
    level_autumn = models.CharField(max_length=10, blank=True)
    level_spring = models.CharField(max_length=10, blank=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    area = models.ForeignKey(PerevalAreas, on_delete=models.SET_NULL, null=True, blank=True)
    images = models.ManyToManyField(PerevalImages)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    moderator_comment = models.TextField(blank=True, null=True)
    moderation_date = models.DateTimeField(blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'pereval_added'
        ordering = ['-date_added']
        verbose_name = 'Перевал'
        verbose_name_plural = 'Перевалы'

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

class SprActivitiesTypes(models.Model):
    """Типы активностей"""
    title = models.TextField()

    class Meta:
        db_table = 'spr_activities_types'

    def __str__(self):
        return self.title