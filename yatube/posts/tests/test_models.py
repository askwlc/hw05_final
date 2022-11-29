from django.conf import settings
from django.test import TestCase

from ..models import Group, Post, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост для теста' * settings.POST_COUNT_FOR_TEST,
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        values = {
            self.post.text[:15]: str(self.post),
            self.group.title: str(self.group),
        }
        for value, expected in values.items():
            with self.subTest(value=value):
                self.assertEqual(value, expected)
