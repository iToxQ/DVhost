"""
Definition of models.
"""

from django.db import models

# Create your models here..
from datetime import datetime
from django.contrib import admin
from django.urls import reverse

from django.contrib.auth.models import User

class Blog(models.Model):
    title = models.CharField(max_length = 100, unique_for_date = "posted", verbose_name = "Заголовок")
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    description = models.TextField(verbose_name = "Краткое содержание")
    content = models.TextField(verbose_name = "Полное содержание")
    file = models.FileField(default = "none.txt", verbose_name = "Путь к файлу")
    posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Опубликована")
    # Методы класса:
    def get_absolute_url(self): # метод возвращает строку с URL-адресом записи
        return reverse("blogpost", args=[str(self.id)])
    def __str__(self): # метод возвращает название, используемое для представления отдельных записей в административном разделе
        return self.title
    # Метаданные – вложенный класс, который задает дополнительные параметры модели:
    class Meta:
        db_table = "Posts" # имя таблицы для модели
        ordering = ["-posted"] # порядок сортировки данных в модели ("-" означает по убыванию)
        verbose_name = "статья блога" # имя, под которым модель будет отображаться в административном разделе (для одной статьи блога)
        verbose_name_plural = "статьи блога" # тоже для всех статей блога

admin.site.register(Blog)

class Comment(models.Model):
    text = models.TextField(verbose_name = "Комментарий",)
    date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата")
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Автор")
    post = models.ForeignKey(Blog, on_delete = models.CASCADE, verbose_name = "Статья")

    def __str__(self):
        return 'Комментарий {} к {}'.format(self.author, self.post)

    class Meta:
        db_table = "Comments" 
        verbose_name = "Комментарий" 
        verbose_name_plural = "Комментарий к статьям блога"
        ordering = ["-date"] 

admin.site.register(Comment) 

class Zakaz(models.Model):
    THEM_CHOICES = (
        ('1', 'Создать файл'),
        ('2', 'Найти файл'),
        ('3', 'Поделиться файлом'),
    )
    STATUS_CHOICES = (
        ('1', 'В ожидании'), 
        ('2', 'Выполнено'),
        ('3', 'Отказ'),
    )

    them = models.CharField(max_length=1, choices=THEM_CHOICES)
    text = models.TextField(verbose_name = "Подробнее о файле",)
    date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата")
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Автор")
    status = models.CharField(default = '1', max_length=1, choices=STATUS_CHOICES)

    def __str__(self):
        return 'Заказ {} №{}'.format(self.author, self.id)

    class Meta:
        db_table = "Zakaz" 
        verbose_name = "Заказ" 
        verbose_name_plural = "Заказы"
        ordering = ["-date"] 

admin.site.register(Zakaz) 