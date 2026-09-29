from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from labels.models import Label
from statuses.models import Status
from tasks.models import Task

User = get_user_model()


class TaskCrudAndFilterTests(TestCase):

    def setUp(self):
        self.tasks_url = reverse('tasks')
        self.task_create_url = reverse('task_create')
        self.login_url = reverse('login')
        
        self.author_user = User.objects.create_user(
            username='author', password='password123'
        )
        self.other_user = User.objects.create_user(
            username='other', password='password456'
        )

        self.status_new = Status.objects.create(title='Новая')
        self.status_done = Status.objects.create(title='Выполнена')
        
        self.label_bug = Label.objects.create(title='Баг')
        self.label_feature = Label.objects.create(title='Фича')
        self.task1 = Task.objects.create(
            title='Задача 1',
            description='Описание 1',
            status=self.status_new,
            author=self.author_user,
            performer=self.other_user,
        )
        self.task1.labels.add(self.label_bug)

        self.task2 = Task.objects.create(
            title='Задача 2',
            description='Описание 2',
            status=self.status_done,
            author=self.other_user,
            performer=self.author_user,
        )
        self.task2.labels.add(self.label_feature)
        self.task1_show_url = reverse(
            'task_show', 
            kwargs={'pk': self.task1.pk}
            )
        self.task1_edit_url = reverse(
            'task_update', kwargs={'pk': self.task1.pk}
        )
        self.task1_delete_url = reverse(
            'task_delete', kwargs={'pk': self.task1.pk}
        )

    def _get_msg_strings(self, response):
        return [msg.message for msg in get_messages(response.wsgi_request)]

    def test_task_list_requires_login(self):
        response = self.client.get(self.tasks_url)
        self.assertRedirects(response, 
        f"{self.login_url}?next={self.tasks_url}")

    def test_task_list_filter_by_status(self):
        self.client.login(username='author', password='password123')
        response = self.client.get(
            self.tasks_url, 
            {'status': self.status_new.pk}
            )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.task1, response.context['tasks'])
        self.assertNotIn(self.task2, response.context['tasks'])

    def test_task_list_filter_by_label(self):
        self.client.login(username='author', password='password123')
        response = self.client.get(
            self.tasks_url, 
            {'label': self.label_bug.pk}
            )
        
        self.assertIn(self.task1, response.context['tasks'])
        self.assertNotIn(self.task2, response.context['tasks'])

    def test_task_list_filter_by_performer(self):
        self.client.login(username='author', password='password123')
        response = self.client.get(
            self.tasks_url, {'performer': self.other_user.pk}
        )
        
        self.assertIn(self.task1, response.context['tasks'])
        self.assertNotIn(self.task2, response.context['tasks'])

    def test_task_list_filter_only_my(self):
        self.client.login(username='author', password='password123')
        response = self.client.get(self.tasks_url, {'only_my': 'on'})
        
        self.assertIn(self.task1, response.context['tasks'])
        self.assertNotIn(self.task2, response.context['tasks'])

    def test_task_show_view(self):
        self.client.login(username='author', password='password123')
        response = self.client.get(self.task1_show_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['task'], self.task1)

    def test_task_create_success(self):
        self.client.login(username='author', password='password123')
        post_data = {
            'title': 'Новая задача тестов',
            'description': 'Какое-то описание',
            'status': self.status_new.pk,
            'performer': self.other_user.pk,
            'labels': [self.label_bug.pk],
        }
        response = self.client.post(self.task_create_url, data=post_data)
        self.assertRedirects(response, self.tasks_url)

        new_task = Task.objects.get(title='Новая задача тестов')
        self.assertEqual(new_task.author, self.author_user)
        
        messages = self._get_msg_strings(response)
        self.assertIn("Задача успешно создана", messages)

    def test_task_update_success(self):
        self.client.login(username='author', password='password123')
        update_data = {
            'title': 'Измененное имя',
            'description': 'Новое описание',
            'status': self.status_done.pk,
            'performer': self.other_user.pk,
            'labels': [self.label_feature.pk],
        }
        response = self.client.post(self.task1_edit_url, data=update_data)
        self.assertRedirects(response, self.tasks_url)

        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, 'Измененное имя')
        
        messages = self._get_msg_strings(response)
        self.assertIn("Задача успешно изменена", messages)

    def test_author_can_delete_task(self):
        self.client.login(username='author', password='password123')
        response = self.client.post(self.task1_delete_url)
        self.assertRedirects(response, self.tasks_url)
        
        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())
        
        messages = self._get_msg_strings(response)
        self.assertIn("Задача успешно удалена", messages)

    def test_non_author_cannot_delete_task(self):
        self.client.login(username='other', password='password456')
        response = self.client.post(self.task1_delete_url)
        
        self.assertRedirects(response, self.tasks_url)
        self.assertTrue(Task.objects.filter(pk=self.task1.pk).exists())
        
        messages = self._get_msg_strings(response)
        self.assertIn("Задачу может удалить только ее автор", messages)