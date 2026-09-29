from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse
from statuses.models import Status
from tasks.models import Task

User = get_user_model()


class StatusCrudTests(TestCase):

    def setUp(self):
        self.statuses_url = reverse('statuses')
        self.status_create_url = reverse('status_create')

        self.user = User.objects.create_user(
            username='testuser', password='password123'
        )

        self.status = Status.objects.create(title='В работе')

        self.status_edit_url = reverse(
            'status_update', kwargs={'pk': self.status.pk}
        )
        self.status_delete_url = reverse(
            'status_delete', kwargs={'pk': self.status.pk}
        )

    def _get_msg_strings(self, response):
        return [msg.message for msg in get_messages(response.wsgi_request)]

    def test_status_list_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.statuses_url)

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.status, response.context['statuses'])

    def test_status_create_success(self):
        self.client.login(username='testuser', password='password123')
        post_data = {
            'title': 'Завершено',
        }
        response = self.client.post(self.status_create_url, data=post_data)
        self.assertRedirects(response, self.statuses_url)

        self.assertTrue(Status.objects.filter(title='Завершено').exists())
        
        messages = self._get_msg_strings(response)
        self.assertIn("Статус успешно создан", messages)

    def test_status_update_success(self):
        self.client.login(username='testuser', password='password123')

        get_response = self.client.get(self.status_edit_url)
        self.assertEqual(get_response.context['ID'], self.status.pk)

        update_data = {
            'title': 'Архив',
        }
        response = self.client.post(self.status_edit_url, data=update_data)
        self.assertRedirects(response, self.statuses_url)

        self.status.refresh_from_db()
        self.assertEqual(self.status.title, 'Архив')

        messages = self._get_msg_strings(response)
        self.assertIn("Статус успешно изменен", messages)

    def test_status_delete_success(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.status_delete_url)
        self.assertRedirects(response, self.statuses_url)

        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())

        messages = self._get_msg_strings(response)
        self.assertIn("Статус успешно удален", messages)

    def test_status_delete_protected_error(self):
        self.client.login(username='testuser', password='password123')

        Task.objects.create(
            title='Связанная задача',
            status=self.status,
            author=self.user
        )

        response = self.client.post(self.status_delete_url)
        self.assertRedirects(response, self.statuses_url)

        self.assertTrue(Status.objects.filter(pk=self.status.pk).exists())

        messages = self._get_msg_strings(response)
        self.assertIn(
            "Невозможно удалить статус, потому что он используется",
            messages
        )