from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class NoteAPITests(APITestCase):

    def test_unauthenticated_user_cannot_access_notes(self):
        url = reverse('note-list')  # جاي من router
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

###############################################3333
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Note

class NotePermissionTests(APITestCase):

    def setUp(self):
        # المستخدم صاحب النوت
        self.owner = User.objects.create_user(
            username="owner",
            password="1234"
        )

        # مستخدم ثاني (المهاجم)
        self.attacker = User.objects.create_user(
            username="attacker",
            password="1234"
        )

        self.note = Note.objects.create(
            title="Secret Note",
            content="Top secret",
            user=self.owner
        )

        self.url = f"/api/notes/{self.note.id}/"

    def test_authenticated_user_cannot_access_other_users_note(self):
        # تسجيل دخول المستخدم غير المالك
        self.client.login(username="attacker", password="1234")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

