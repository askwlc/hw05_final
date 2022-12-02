from django.contrib.auth import get_user_model
from django.db import models

from core.models import CreatedModel

User = get_user_model()


class Group(models.Model):
    """Модель для управления группами."""
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, verbose_name='Ссылка')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Группы'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Post(CreatedModel):
    """Модель для хранения постов."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name="posts",
        blank=True,
        null=True,
        verbose_name='Группа',
        help_text='Выберите группу'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Сообщение пользователя'
        verbose_name_plural = 'Сообщения пользователей'

    def __str__(self):
        return self.text[:15]


class Comment(CreatedModel):
    """Модель для хранения комментариев."""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий пользователя'
        verbose_name_plural = 'Комментарии пользователей'

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписант'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follows'
            )]

    def __str__(self):
        return f'{self.user} подписался на {self.author}'
