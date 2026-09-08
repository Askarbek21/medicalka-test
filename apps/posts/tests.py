from django.urls import reverse

from rest_framework.test import APITestCase

from apps.auth.models import User

from .models import Post, Like
from .services import comment_create


class PostLikesTests(APITestCase):

    def setUp(self):
        self.author = User.objects.create_user(
            full_name='author authorovich',
            email='author@gmail.com',
            username='author',
            password='qwerty123',
            is_verified=True,
        )

        self.verified_user = User.objects.create_user(
            full_name='user userovich',
            email='user@gmail.com',
            username='user',
            password='qwerty123',
            is_verified=True,
        )

        self.unverified_user = User.objects.create_user(
            full_name='unverified userovich',
            email='unverified@gmail.com',
            username='unverified',
            password='qwerty123',
            is_verified=False,
        )

        self.post = Post.objects.create(
            author=self.author,
            title='test post',
            content='content',
        )


    def test_user_can_like_post(self):
        self.client.force_authenticate(user=self.verified_user)

        response = self.client.post(
            reverse(
                'post-like',
                kwargs={'post_id': self.post.id},
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            Like.objects.count(),
            1,
        )


    def test_user_cannot_like_own_post(self):
        self.client.force_authenticate(user=self.author)

        response = self.client.post(
            reverse(
                'post-like',
                kwargs={'post_id': self.post.id},
            )
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.assertEqual(
            Like.objects.count(),
            0,
        )


    def test_user_cannot_like_post_twice(self):
        self.client.force_authenticate(user=self.verified_user)

        like_url = reverse(
            'post-like',
            kwargs={'post_id': self.post.id},
        )

        first_response = self.client.post(like_url)

        second_response = self.client.post(like_url)

        self.assertEqual(
            first_response.status_code,
            200,
        )

        self.assertEqual(
            second_response.status_code,
            400,
        )

        self.assertEqual(
            Like.objects.count(),
            1,
        )


    def test_unverified_user_cannot_create_post(self):
        self.client.force_authenticate(user=self.unverified_user)

        response = self.client.post(
            reverse('post-create'),
            {
                'title': 'test title',
                'content': 'content',
            },
            format='json',
        )

        self.assertEqual(response.status_code, 403)
    

    def test_verified_user_can_create_post(self):
        self.client.force_authenticate(user=self.verified_user)

        response = self.client.post(
            reverse('post-create'),
            {
                'title': 'test title',
                'content': 'content',
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 2) # 2 изза фикстуры 
    

    def test_unverified_user_cannot_create_comment(self):
        self.client.force_authenticate(user=self.unverified_user)

        response = self.client.post(
            reverse(
                'comment-create',
                kwargs={'post_id': self.post.id},
            ),
            {'content': 'asdasd'},
            format='json',
        )

        self.assertEqual(response.status_code, 403)
    

    def test_user_cannot_update_other_post(self):
        self.client.force_authenticate(user=self.verified_user)

        response = self.client.patch(
            reverse(
                'post-update',
                kwargs={'post_id': self.post.id},
            ),
            {'title': 'dsadasd'},
            format='json',
        )

        self.assertEqual(response.status_code, 403)


    def test_user_cannot_delete_other_post(self):
        self.client.force_authenticate(user=self.verified_user)

        response = self.client.delete(
            reverse(
                'post-delete',
                kwargs={'post_id': self.post.id},
            )
        )

        self.assertEqual(response.status_code, 403)


    def test_user_cannot_delete_other_comment(self):
        comment = comment_create(
            post=self.post,
            author=self.author,
            content='comment',
        )

        self.client.force_authenticate(user=self.verified_user)

        response = self.client.delete(
            reverse(
                'comment-delete',
                kwargs={
                    'post_id': self.post.id,
                    'comment_id': comment.id,
                },
            )
        )

        self.assertEqual(response.status_code, 403)