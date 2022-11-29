import tempfile
from http import HTTPStatus

from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Comment, Follow, Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='testuser')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='group_slug',
            description='Тестовое описание'
        )
        cls.edited_group = Group.objects.create(
            title='Название группы после редактирования',
            slug='test-edited',
            description='Тестовое описание группы после редактирования'
        )
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name="small.gif",
            content=small_gif,
            content_type="image/gif",
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Текст для поста',
            group=cls.group,
            image=uploaded
        )

    def setUp(self):
        super().setUp()
        self.guest_user = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Тест создания поста"""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый пост',
            'group': self.group.id,
            "image": self.post.image
        }

        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:profile',
            args=(self.user,)
        ))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        post = Post.objects.latest('id')
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.author, self.user)
        self.assertEqual(form_data['image'], "posts/small.gif")

    def test_edit_post(self):
        """Тест редактирования поста авториз. пользователем"""
        test_group = Group.objects.create(
            title="Заголовок для тестовой группы",
            slug="test_group_slug"
        )
        form_data = {
            'text': 'Отредактированный текст поста',
            'group': test_group.id
        }
        response = self.authorized_client.post(
            reverse(
                'posts:post_edit',
                args=[self.post.id]),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail', args=(self.post.id,))
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.post.refresh_from_db()
        post = Post.objects.latest('id')
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.group_id, form_data['group'])

    def test_no_edit_post(self):
        """Тест редактирования неавториз. пользователем"""
        posts_count = Post.objects.count()
        form_data = {'text': 'Отредактированный текст поста',
                     'group': self.edited_group.id
                     }
        response = self.guest_user.post(
            reverse('posts:post_edit', args=(self.post.id,)),
            data=form_data, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        error = 'Поcт добавлен в базу данных ошибочно'
        self.assertNotEqual(Post.objects.count(),
                            posts_count + 1,
                            error)
        edited_post = Post.objects.get(id=self.post.id)
        self.assertNotEqual(edited_post.text, form_data['text'])
        self.assertNotEqual(edited_post.group.id, form_data['group'])


class CommentCreateExistTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser')
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.post_test = Post.objects.create(
            text='Тестовый пост контент',
            author=cls.user
        )
        cls.comment_test = Comment.objects.create(
            text='Тестовый комментарий',
            post=cls.post_test,
            author=cls.user
        )

    def test_authorized_comment_add(self):
        """Тест добавления комментария авториз. пользователем."""
        comments_count = Comment.objects.count()
        user = User.objects.create(username='user')
        form_data = {
            'text': 'Тестовый комментарий 1',
            'author': user
        }
        self.authorized_client.force_login(user)
        self.authorized_client.post(
            reverse('posts:add_comment', args=(self.post_test.pk,)),
            data=form_data,
            follow=True
        )
        self.assertEqual(Comment.objects.count(), comments_count + 1)
        self.assertEqual(Comment.objects.first().text, form_data['text'])


class FollowTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post_autor = User.objects.create(username='autor')
        cls.post_follower = User.objects.create(username='follower')
        cls.post = Post.objects.create(text='Подпишись на меня',
                                       author=cls.post_autor,)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.post_follower)
        self.follower_client = Client()
        self.follower_client.force_login(self.post_autor)
        cache.clear()

    def test_follow_on_user(self):
        """Проверка подписки на пользователя."""
        count_follow = Follow.objects.count()
        self.follower_client.post(
            reverse('posts:profile_follow',
                    kwargs={'username': self.post_follower}))
        follow = Follow.objects.all().latest('id')
        self.assertEqual(Follow.objects.count(), count_follow + 1)
        self.assertEqual(follow.author_id, self.post_follower.id)
        self.assertEqual(follow.user_id, self.post_autor.id)

    def test_unfollow_on_user(self):
        """Проверка отписки от пользователя."""
        Follow.objects.create(user=self.post_autor,
                              author=self.post_follower)
        count_follow = Follow.objects.count()
        self.follower_client.post(
            reverse('posts:profile_unfollow',
                    kwargs={'username': self.post_follower}))
        self.assertEqual(Follow.objects.count(), count_follow - 1)
