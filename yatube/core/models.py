from django.db import models


class CreatedModel(models.Model):
    """Абстрактная модель даты создания"""
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    text = models.TextField(
        verbose_name='Текст',
        help_text='Введите текст'
    )

    class Meta:
        abstract = True
