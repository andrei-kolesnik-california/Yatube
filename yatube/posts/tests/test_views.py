import shutil
import tempfile
from PIL import Image
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django import forms
from posts.models import Post, Group, Follow

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='StasBasov')
        cls.additional_user = User.objects.create_user(username='AhmedAtmanov')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='AK',
            description='Тестовое описание',
        )
        cls.additional_group = Group.objects.create(
            title='Дополнительная тестовая группа',
            slug='AA',
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
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )

        posts_list = []
        for index in range(1, 14):
            posts_list.append(Post(
                text='Текст' + str(index),
                author=cls.user,
                group=cls.group,
                image=cls.uploaded
            ))
        for index in range(14, 27):
            posts_list.append(Post(
                text='Текст' + str(index),
                author=cls.additional_user,
                group=cls.additional_group,
                image=cls.uploaded
            ))
        Post.objects.bulk_create(posts_list)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': 'AK'}): (
                'posts/group_list.html'
            ),
            reverse('posts:profile', kwargs={'username': self.user}): (
                'posts/profile.html'
            ),
            reverse('posts:post_detail', kwargs={'post_id': '1'}): (
                'posts/post_detail.html'
            ),
            reverse('posts:post_edit', kwargs={'post_id': '1'}): (
                'posts/create_post.html'
            ),
            reverse('posts:post_create'): 'posts/create_post.html'
        }

        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        post_image_0 = first_object.image
        post_author_0 = str(first_object.author)
        post_group_0 = str(first_object.group)
        self.assertEqual(post_text_0, 'Текст26')
        self.assertIsNotNone(Image.open(post_image_0))
        self.assertEqual(post_author_0, str(self.additional_user))
        self.assertEqual(post_group_0, str(self.additional_group))

    def test_first_index_page_contains_ten_records(self):
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_third_index_page_contains_six_records(self):
        response = self.client.get(reverse('posts:index') + '?page=3')
        self.assertEqual(len(response.context['page_obj']), 6)

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
        )
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        post_image_0 = first_object.image
        post_author_0 = str(first_object.author)
        post_group_0 = str(first_object.group)
        self.assertEqual(post_text_0, 'Текст13')
        self.assertIsNotNone(Image.open(post_image_0))
        self.assertEqual(post_author_0, str(self.user))
        self.assertEqual(post_group_0, str(self.group))

    def test_first_group_list_page_contains_ten_records(self):
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
        )
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_group_list_contains_three_records(self):
        response = self.client.get(
            reverse('posts:group_list', kwargs={'slug': 'AK'}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={
                    'username': str(self.additional_user)})
        )
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        post_image_0 = first_object.image
        post_author_0 = str(first_object.author)
        post_group_0 = str(first_object.group)
        self.assertEqual(post_text_0, 'Текст26')
        self.assertIsNotNone(Image.open(post_image_0))
        self.assertEqual(post_author_0, str(self.additional_user))
        self.assertEqual(post_group_0, str(self.additional_group))

    def test_first_profile_page_contains_ten_records(self):
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={
                    'username': str(self.additional_user)})
        )
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_profile_contains_three_records(self):
        response = self.client.get(
            reverse('posts:profile', kwargs={
                    'username': str(self.additional_user)}) + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        post = Post.objects.get(pk=26)
        form_data = {
            'text': 'Еще комментарий',
            'post': post
        }
        self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': post.pk}),
            data=form_data
        )
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': '26'})
        )
        object_post = response.context['post']
        post_text_0 = object_post.text
        post_image_0 = object_post.image
        post_author_0 = str(object_post.author)
        post_group_0 = str(object_post.group)
        self.assertEqual(post_text_0, 'Текст26')
        self.assertIsNotNone(Image.open(post_image_0))
        self.assertEqual(post_author_0, str(self.additional_user))
        self.assertEqual(post_group_0, str(self.additional_group))
        object_comment = response.context['comments']
        comment_text_0 = object_comment[0].text
        self.assertEqual(comment_text_0, 'Еще комментарий')

    def test_post_edit_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': '26'})
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_create_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_index_page_cashed(self):
        """Тестирования кеширования главной страницы."""
        response = self.authorized_client.get(reverse('posts:index'))
        Post.objects.all().delete()
        response_one_more = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(response.content, response_one_more.content)
        cache.clear()
        response_cleared = self.authorized_client.get(reverse('posts:index'))
        self.assertNotEqual(response.content, response_cleared.content)

    def test_profile_follow(self):
        """Тестирование добавления подписки."""
        additional_username = self.additional_user.get_full_name()
        self.authorized_client.post(
            reverse('posts:profile_follow', kwargs={
                    'username': self.additional_user}),
            data={'username': additional_username}
        )
        username = self.user.get_full_name()
        self.guest_client.post(
            reverse('posts:profile_follow', kwargs={
                    'username': self.additional_user}),
            data={'username': username}
        )
        counter = Follow.objects.all().count()
        # проверка одной добавленной подписки от авторизованного пользователя
        self.assertEqual(counter, 1)

    def test_profile_unfollow(self):
        """Тестирование удаления подписки."""
        username = self.additional_user.get_full_name()
        self.authorized_client.post(
            reverse('posts:profile_follow', kwargs={
                    'username': self.additional_user}),
            data={'username': username}
        )
        counter = Follow.objects.all().count()
        self.assertEqual(counter, 1)
        self.authorized_client.delete(
            reverse('posts:profile_unfollow', kwargs={
                    'username': self.additional_user}),
            data={'username': username}
        )
        counter = Follow.objects.all().count()
        self.assertEqual(counter, 0)

    def test_follow_index(self):
        """Новая запись появляется только у подписанного пользователя."""
        additional_username = self.additional_user.get_full_name()
        self.authorized_client.post(
            reverse('posts:profile_follow', kwargs={
                    'username': self.additional_user}),
            data={'username': additional_username}
        )
        Post.objects.create(
            text='Тестовый текст!!!',
            author=self.additional_user,
            group=self.group
        )
        response = self.authorized_client.get(reverse('posts:follow_index'))
        result = False
        for object in response.context['page_obj']:
            if 'Тестовый текст!!!' == object.text:
                result = True
        # если пост с текстом найден в объекте ответа авторизованного юзера
        # то тест будет пройден
        self.assertTrue(result)
        response = self.guest_client.get(reverse('posts:follow_index'))
        self.assertEqual(response.context, None)
