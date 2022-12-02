from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from posts.forms import PostForm
from posts.models import Follow, Group, Post, User


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='testuser')
        cls.post_follower = User.objects.create(username='follower')
        Follow.objects.create(user=cls.post_follower,
                              author=cls.user)
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='testslug',
            description='Тестовое описание',
        )
        cls.posts = []
        for i in range(settings.POST_COUNT_FOR_TEST):
            cls.posts.append(
                Post(
                    text=f'Тестовый текст {i}',
                    author=cls.user,
                    group=cls.group
                )
            )
        Post.objects.bulk_create(cls.posts)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.post_follower_client = Client()
        self.post_follower_client.force_login(self.post_follower)

    def test_correct_page_context_guest_client(self):
        pages = [
            reverse('posts:index'),
            reverse(
                'posts:profile',
                args=(self.user.username,)
            ),
            reverse(
                'posts:group_list',
                args=(self.group.slug,)
            ),
            reverse(
                'posts:follow_index'
            )]
        tests_pages = [
            (settings.POST_COUNT, 1),
            (Post.objects.count() - settings.POST_COUNT, 2)
        ]
        for posts_count, page_number in tests_pages:
            for page in pages:
                with self.subTest(page=page):
                    response = self.post_follower_client.get(
                        page, {'page': page_number}
                    )
                    self.assertEqual(
                        posts_count,
                        len(response.context['page_obj']),
                    )


class PostsViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='slug_slug',
            description='Тестовое описание',
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
            text='Тестовый пост',
            group=cls.group,
            image=uploaded
        )

    def setUp(self) -> None:
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_correct_templates_for_names(self):
        """Тест шаблонов по name"""
        post = Post.objects.create(
            author=self.user,
            text='Тестовый пост',
        )
        templates_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', args=(
                    f'{self.group.slug}',)): 'posts/group_list.html',
            reverse('posts:profile', args=(
                    f'{self.user.username}',)): 'posts/profile.html',
            reverse('posts:post_detail', args=(
                    f'{post.id}',)): 'posts/post_detail.html',
            reverse('posts:post_edit', args=(
                    f'{post.id}',)): 'posts/create_post.html',
        }
        for url, template in templates_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def custom_test_page_show_correct_context(self, first_object):
        self.assertEqual(first_object.author.username, self.user.username)
        self.assertEqual(first_object.text, 'Тестовый пост')
        self.assertEqual(first_object.group, self.group)
        self.assertEqual(first_object.image, self.post.image)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 1)
        first_object = response.context['page_obj'][0]
        self.custom_test_page_show_correct_context(first_object)

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:group_list', args=(self.group.slug,)))
        self.assertEqual(len(response.context['page_obj']), 1)
        first_object = response.context['page_obj'][0]
        self.custom_test_page_show_correct_context(first_object)
        self.assertEqual(response.context['group'], self.group)

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:profile', args=(self.user,)))
        self.assertEqual(len(response.context['page_obj']), 1)
        first_object = response.context['page_obj'][0]
        self.custom_test_page_show_correct_context(first_object)
        self.assertEqual(response.context['author'], self.user)

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:post_detail', args=(self.post.pk,)))
        first_object = response.context['post']
        self.custom_test_page_show_correct_context(first_object)

    def test_create_post_show_correct_context(self):
        """Шаблон create_post сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        self.assertIsInstance(response.context.get('form'), PostForm)

    def test_post_edit_page_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом"""
        response = self.authorized_client.get(
            reverse('posts:post_edit',
                    args=(self.post.pk,)
                    )
        )
        self.assertTrue(response.context.get('is_edit'))
        self.assertIsInstance(response.context.get('form'), PostForm)
        self.assertEqual(response.context.get('form').instance, self.post)

    def test_post_not_get_another_group(self):
        """Созданный пост не попал в другую группу"""
        response = self.authorized_client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug}
            )
        )
        post_object = response.context['page_obj']
        self.assertNotIn(self.post.group, post_object)

    def test_cache_index_page(self):
        """Главная страница корректно кэширует список записей."""
        post = Post.objects.create(
            text='Тестовый пост',
            author=self.user)
        content_add = self.authorized_client.get(
            reverse('posts:index')).content
        post.delete()
        content_delete = self.authorized_client.get(
            reverse('posts:index')).content
        self.assertEqual(content_add, content_delete)
        cache.clear()
        content_cache_clear = self.authorized_client.get(
            reverse('posts:index')).content
        self.assertNotEqual(content_add, content_cache_clear)


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

    def test_subscription(self):
        """Запись появляется в ленте подписчиков."""
        Follow.objects.create(
            user=self.post_follower,
            author=self.post_autor
        )
        response = self.authorized_client.get('/follow/')
        post_text_0 = response.context['page_obj'][0].text
        self.assertEqual(post_text_0, 'Подпишись на меня')

    def test_posts_on_unfollowers(self):
        """Проверка записей у тех кто не подписан на авторов."""
        post = Post.objects.create(
            author=self.post_autor,
            text='Тестовый текст'
        )
        response = self.authorized_client.get(
            reverse('posts:follow_index')
        )
        post_object = response.context['page_obj']
        self.assertNotIn(post, post_object)
