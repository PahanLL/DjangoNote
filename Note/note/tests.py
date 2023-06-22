from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from note.models import Group, Note

class NotesTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='Pashka_123')
        self.client.login(username='testuser', password='Pashka_123')

        self.group = Group.objects.create(name='Test Group', created_by=self.user)
        self.note = Note.objects.create(title='Test Note', content='Test Content', category='WORK', created_by=self.user, group=self.group)

    def test_note_list(self):
        response = self.client.get(reverse('note:note_list'))
        self.assertEqual(response.status_code, 200)

    def test_note_edit(self):
        response = self.client.get(reverse('note:note_edit', args=(self.note.id,)))
        self.assertEqual(response.status_code, 200)

    def test_note_delete(self):
        response = self.client.get(reverse('note:note_delete', args=(self.note.id,)))
        self.assertEqual(response.status_code, 302)

