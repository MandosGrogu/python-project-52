from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from labels.models import Label
from statuses.models import Status
from tasks.models import Task

User = get_user_model()


class LabelCrudTests(TestCase):

    def setUp(self):
        self.labels_url = reverse('labels')
        self.label_create_url = reverse('label_create')

        self.user = User.objects.create_user(
            username='testuser', password='password123'
        )

        self.label = Label.objects.create(title='Важно')

        self.label_edit_url = reverse(
            'label_update', kwargs={'pk': self.label.pk}
        )
        self.label_delete_url = reverse(
            'label_delete', kwargs={'pk': self.label.pk}
        )

    def _get_msg_strings(self, response):
        return [msg.message for msg in get_messages(response.wsgi_request)]

    def test_label_list_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.labels_url)

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.label, response.context['labels'])

    def test_label_create_success(self):
        self.client.login(username='testuser', password='password123')
        post_data = {
            'title': 'Документация',
        }
        response = self.client.post(self.label_create_url, data=post_data)
        self.assertRedirects(response, self.labels_url)

        self.assertTrue(Label.objects.filter(title='Документация').exists())

        messages = self._get_msg_strings(response)
        self.assertIn("Метка успешно создана", messages)

    def test_label_update_success(self):
        self.client.login(username='testuser', password='password123')

        get_response = self.client.get(self.label_edit_url)
        self.assertEqual(get_response.context['ID'], self.label.pk)

        update_data = {
            'title': 'Срочно',
        }
        response = self.client.post(self.label_edit_url, data=update_data)
        self.assertRedirects(response, self.labels_url)

        self.label.refresh_from_db()
        self.assertEqual(self.label.title, 'Срочно')

        messages = self._get_msg_strings(response)
        self.assertIn("Метка успешно изменена", messages)

    def test_label_delete_success(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.label_delete_url)
        self.assertRedirects(response, self.labels_url)

        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())

        messages = self._get_msg_strings(response)
        self.assertIn("Метка успешно удалена", messages)

    def test_label_delete_protected_error(self):
        self.client.login(username='testuser', password='password123')

        test_status = Status.objects.create(title='В планах')

        task = Task.objects.create(
            title='Тестовая задача',
            author=self.user,
            status=test_status
        )
        task.labels.add(self.label)

        response = self.client.post(self.label_delete_url)
        self.assertRedirects(response, self.labels_url)

        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())

        messages = self._get_msg_strings(response)
        self.assertIn(
            "Невозможно удалить метку, потому что она используется",
            messages
        )