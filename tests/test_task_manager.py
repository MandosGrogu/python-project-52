from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

User = get_user_model()

class UserAuthAndCrudTests(TestCase):

    def setUp(self):
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.signup_url = reverse('signup')
        self.users_url = reverse('users')
        self.index_url = reverse('index')

        self.user1_data = {
            'username': 'testuser1',
            'password': 'password123',
        }
        self.user2_data = {
            'username': 'testuser2',
            'password': 'password456',
        }

        self.user1 = User.objects.create_user(**self.user1_data)
        self.user2 = User.objects.create_user(**self.user2_data)

        self.delete_user1_url = reverse(
            'delete', kwargs={'pk': self.user1.pk}
        )
        self.update_user1_url = reverse(
            'update', kwargs={'pk': self.user1.pk}
        )

    def _get_msg_strings(self, response):
        return [msg.message for msg in get_messages(response.wsgi_request)]

    def test_login_view_success(self):
        response = self.client.post(self.login_url, self.user1_data)
        self.assertRedirects(response, self.index_url)

        messages = self._get_msg_strings(response)
        self.assertIn("Вы залогинены", messages)

    def test_logout_view_success(self):
        self.client.login(**self.user1_data)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)

        messages = self._get_msg_strings(response)
        self.assertIn("Вы разлогинены", messages)

    def test_signup_view_success(self):
        new_user_data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'password1': 'newpassword123',
        }
        post_data = {
            'username': new_user_data['username'],
            'password1': new_user_data['password'],
            'password2': new_user_data['password1'],
        }
        response = self.client.post(self.signup_url, data=post_data)
        self.assertRedirects(response, self.login_url)
        self.assertTrue(
            User.objects.filter(username='newuser').exists()
        )

        messages = self._get_msg_strings(response)
        self.assertIn("Пользователь успешно зарегистрирован", messages)

    def test_user_can_update_themselves(self):
        self.client.login(**self.user1_data)
        update_data = {
            'username': 'updated_name',
            'password1': 'new_secure_pass123',
            'password2': 'new_secure_pass123',
        }
        response = self.client.post(self.update_user1_url, data=update_data)
        self.assertRedirects(response, self.users_url)

        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, 'updated_name')

        messages = self._get_msg_strings(response)
        self.assertIn("Пользователь успешно изменен", messages)

    def test_user_cannot_update_other_user(self):
        self.client.login(**self.user2_data)
        update_data = {
            'username': 'hacked_name',
        }
        response = self.client.post(self.update_user1_url, data=update_data)
        self.assertRedirects(response, self.users_url)

        self.user1.refresh_from_db()
        self.assertNotEqual(self.user1.username, 'hacked_name')

        messages = self._get_msg_strings(response)
        self.assertIn("У вас нет прав для изменения", messages)

    def test_user_can_delete_themselves(self):
        self.client.login(**self.user1_data)
        response = self.client.post(self.delete_user1_url)
        self.assertRedirects(response, self.users_url)
        self.assertFalse(
            User.objects.filter(pk=self.user1.pk).exists()
        )

        messages = self._get_msg_strings(response)
        self.assertIn("Пользователь успешно удален", messages)

    def test_user_cannot_delete_other_user(self):
        """Пользователь не может удалить чужой аккаунт."""
        self.client.login(**self.user2_data)
        response = self.client.post(self.delete_user1_url)
        self.assertRedirects(response, self.users_url)
        self.assertTrue(
            User.objects.filter(pk=self.user1.pk).exists()
        )

        messages = self._get_msg_strings(response)
        self.assertIn("У вас нет прав для изменения", messages)