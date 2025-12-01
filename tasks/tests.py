from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskViewsTestCase(TestCase):
    """Test case for task views."""

    def setUp(self):
        """Set up test data."""
        self.task1 = Task.objects.create(title="Test Task 1", complete=False)
        self.task2 = Task.objects.create(title="Test Task 2", complete=True)

    def test_index_view(self):
        """Test the index view (/)."""
        response = self.client.get(reverse('list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task 1")
        self.assertContains(response, "Test Task 2")
        self.assertTemplateUsed(response, 'tasks/list.html')

    def test_index_view_post(self):
        """Test creating a task via POST to index view."""
        response = self.client.post(reverse('list'), {'title': 'New Task'})
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_update_task_view_get(self):
        """Test the update task view GET request."""
        response = self.client.get(
            reverse('update_task', kwargs={'pk': self.task1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/update_task.html')
        self.assertContains(response, "Test Task 1")

    def test_update_task_view_post(self):
        """Test updating a task via POST."""
        response = self.client.post(
            reverse('update_task', kwargs={'pk': self.task1.id}),
            {'title': 'Updated Task', 'complete': True}
        )
        self.assertEqual(response.status_code, 302)  # Redirect
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, 'Updated Task')
        self.assertTrue(self.task1.complete)

    def test_delete_task_view_get(self):
        """Test the delete task view GET request."""
        response = self.client.get(
            reverse('delete', kwargs={'pk': self.task1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/delete.html')

    def test_delete_task_view_post(self):
        """Test deleting a task via POST."""
        task_id = self.task1.id
        response = self.client.post(
            reverse('delete', kwargs={'pk': task_id})
        )
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertFalse(Task.objects.filter(id=task_id).exists())


class TaskModelTestCase(TestCase):
    """Test case for Task model."""

    def test_task_creation(self):
        """Test creating a task."""
        task = Task.objects.create(title="Test Task")
        self.assertEqual(task.title, "Test Task")
        self.assertFalse(task.complete)
        self.assertIsNotNone(task.created)

    def test_task_str(self):
        """Test the string representation of a task."""
        task = Task.objects.create(title="Test Task")
        self.assertEqual(str(task), "Test Task")


class DatasetImportTestCase(TestCase):
    """Test case for dataset import."""

    fixtures = ['dataset.json']

    def test_dataset_import(self):
        """Test that the dataset is correctly imported."""
        # Check that tasks were imported
        self.assertEqual(Task.objects.count(), 5)

        # Check specific tasks
        task1 = Task.objects.get(pk=1)
        self.assertEqual(task1.title, "Complete Django tutorial")
        self.assertFalse(task1.complete)

        task2 = Task.objects.get(pk=2)
        self.assertEqual(task2.title, "Write unit tests")
        self.assertTrue(task2.complete)

        task5 = Task.objects.get(pk=5)
        self.assertEqual(task5.title, "Update documentation")
        self.assertTrue(task5.complete)
