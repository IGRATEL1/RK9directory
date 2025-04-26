from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from RK9directory import settings

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
        .filter(status=Materials_stats.Status.PUBLISHED)

class Materials_stats(models.Model):
    class Meta:
        ordering = ['title']#сортируем по названию по алфавиту
        indexes =   [
                    models.Index(fields=['-publish']),#id моделей по дате публикации
                    ]
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'#в базе данных будут хранится еще не подтвержденные материалы

    title=models.CharField(max_length=250)#название материала

    strength_limit = models.CharField(max_length=10)#предел прочности

    modulus_of_elasticity = models.CharField(max_length=10)#модуль упругости

    yield_strength = models.CharField(max_length=10)#предел текучести

    elongation = models.CharField(max_length=5)#относительное удлинение

    poisson_ratio = models.CharField(max_length=10)#коэффициент Пуассона

    ansys_file = models.FileField(upload_to='files')#файл ансиса

    ludwig_const= models.CharField(max_length=6)

    material_hardening_index = models.CharField(max_length=10)

    publish = models.DateTimeField(default=timezone.now)#время публикации

    created = models.DateTimeField(auto_now_add=True)#время записи

    updated = models.DateTimeField(auto_now=True)#время обновления
    
    status = models.CharField(max_length=2,
                                    choices=Status.choices,
                                    default=Status.DRAFT)#статус публикации
    author = models.ForeignKey(User,
                                on_delete=models.RESTRICT)
    objects = models.Manager() # менеджер, применяемый по умолчанию
    published = PublishedManager() # конкретно-прикладной менеджер

    graph_file = models.FileField(upload_to='graphs', default='settings.MEDIA_ROOT/files/sad_face.png')

    threeD_model = models.FileField(upload_to='3Dmodel')
    def get_absolute_url(self):
        return reverse('db_list:material_detail',
            args=[self.id])

class Members(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        verbose_name='User', help_text='User who belongs to this project',
        related_name='projects',
    )
    project = models.ForeignKey(
        Materials_stats, on_delete=models.CASCADE,
        verbose_name='Project', help_text='Project to which this user belongs',
        related_name='users',
    )
    allow_change = models.BooleanField(
        default=True,
        verbose_name='Allow Change',
        help_text='Is the member allowed to change the project data?'
    )
    allow_manage = models.BooleanField(
        default=False,
        verbose_name='Allow Manage',
        help_text='Is the member allowed to manage users for the project?'
    )  