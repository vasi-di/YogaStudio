from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Profile

UserModel = get_user_model()


class ProfileTests(TestCase):

    def setUp(self):
        self.user = UserModel.objects.create_user(email="test@test.com", password="password123")
        self.user2 = UserModel.objects.create_user(email="test2@test.com", password="password123")

        self.profile = Profile.objects.create(user=self.user)
        self.profile2 = Profile.objects.create(user=self.user2)

        self.client.login(email="test@test.com", password="password123")

        self.profile_url = reverse("profile_detail", kwargs={'pk': self.profile.pk})
        self.profile_edit_url = reverse("profile_edit", kwargs={'pk': self.profile.pk})

    def test_create_profile_on_user_creation(self):
        new_user = UserModel.objects.create_user(email="new_user@test.com", password="password123")
        profile = Profile.objects.create(user=new_user)
        self.assertEqual(profile.user, new_user)

    def test_profile_creation(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile_detail.html')
        self.assertContains(response, self.user.email)

    def test_update_profile(self):
        updated_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'profile_picture': 'http://test.com/pic.jpg'
        }
        response = self.client.post(self.profile_edit_url, updated_data)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.first_name, 'John')
        self.assertEqual(self.profile.last_name, 'Doe')
        self.assertEqual(self.profile.profile_picture, 'http://test.com/pic.jpg')
        self.assertRedirects(response, self.profile_url)

    def test_only_user_can_edit_their_profile(self):
        self.client.login(email="test@test.com", password="password123")
        response = self.client.get(reverse('profile_edit', kwargs={'pk': self.profile.pk}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('profile_edit', kwargs={'pk': self.profile2.pk}))
        self.assertEqual(response.status_code, 403)