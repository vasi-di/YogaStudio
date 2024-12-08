from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import YogaClass, Booking, Review
from .forms import YogaClassBookingForm
from django.utils.timezone import now, timedelta


class BookingModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email="test@test.com", password="password123")
        self.yoga_class = YogaClass.objects.create(
            name="Morning Yoga",
            schedule=now() + timedelta(days=1),
            level="Beginner",
            studio="Earth",
            description="Start your day with yoga."
        )

    def test_booking_status_based_on_total_bookings(self):
        for i in range(20):
            Booking.objects.create(user=self.user, yoga_class=self.yoga_class)
            last_booking = self.yoga_class.bookings.last()
            if i < 2:
                self.assertEqual(last_booking.status, "pending")
            elif 2 <= i < 19:
                self.assertEqual(last_booking.status, "confirmed")
            else:
                self.assertEqual(last_booking.status, "cancelled")


class YogaClassBookingFormTest(TestCase):
    def setUp(self):
        self.yoga_class = YogaClass.objects.create(
            name="Morning Yoga",
            schedule=now() + timedelta(days=1),
            level="Beginner",
            studio="Earth",
            description="Start your day with yoga."
        )

    def test_form_initialization_with_yoga_class_id(self):
        form = YogaClassBookingForm(yoga_class_id=self.yoga_class.id)
        self.assertEqual(form.fields["yoga_class"].initial, self.yoga_class)

    def test_form_queryset_includes_all_classes(self):
        form = YogaClassBookingForm()
        self.assertIn(self.yoga_class, form.fields["yoga_class"].queryset)


class BookingCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email="test@test.com", password="password123")
        self.yoga_class = YogaClass.objects.create(
            name="Morning Yoga",
            schedule=now() + timedelta(days=1),
            level="Beginner",
            studio="Earth",
            description="Start your day with yoga."
        )
        self.url = reverse("book_class", kwargs={"yoga_class_id": self.yoga_class.id})

    def login_and_post(self, user, yoga_class_id=None, schedule=None):
        self.client.login(email=user.email, password="password123")
        return self.client.post(self.url, {"yoga_class": yoga_class_id or self.yoga_class.id,
                                           "booking_date": schedule or self.yoga_class.schedule})

    def assert_form_error(self, response, field, expected_message):
        form = response.context.get("form")
        self.assertIsNotNone(form, "The form is not included in the response context.")
        self.assertTrue(form.errors, "No errors were found in the form.")
        self.assertIn(field, form.errors, f"The '{field}' field did not have errors.")
        self.assertIn(expected_message, form.errors[field],
                      f"The expected error message is missing from the '{field}' field.")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_successful_booking(self):
        response = self.login_and_post(self.user)
        self.assertEqual(Booking.objects.count(), 1, "The booking was not created.")
        self.assertRedirects(response, reverse("profile_detail", kwargs={"pk": self.user.pk}))

    def test_prevent_duplicate_booking(self):
        Booking.objects.create(user=self.user, yoga_class=self.yoga_class)
        response = self.login_and_post(self.user)
        self.assert_form_error(response, "yoga_class", "You have already booked this class!")

    def test_prevent_overbooking(self):
        for _ in range(20):
            Booking.objects.create(user=get_user_model().objects.create_user(
                email=f"user{_}@test.com", password="password123"), yoga_class=self.yoga_class)
        response = self.login_and_post(self.user)
        self.assert_form_error(response, "yoga_class",
                               "Sorry, this class is fully booked. Please select another class.")


class ReviewViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email="test@test.com", password="password123")
        self.yoga_class = YogaClass.objects.create(
            name="Morning Yoga",
            schedule="2024-11-30 08:00:00",
            level="Beginner",
            studio="Earth",
            description="Start your day with yoga."
        )
        self.review_data = {
            "yoga_class": self.yoga_class.id,
            "rating": 5,
            "comments": "Great class!"
        }
        self.list_url = reverse("review_list")
        self.create_url = reverse("add_review")
        self.client.login(email="test@test.com", password="password123")

    def assertReviewExists(self, rating, comments, user=None, yoga_class=None):
        user = user or self.user
        yoga_class = yoga_class or self.yoga_class
        self.assertTrue(
            Review.objects.filter(user=user, yoga_class=yoga_class, rating=rating, comments=comments).exists(),
            "The expected review does not exist in the database."
        )

    def test_create_review(self):
        response = self.client.post(self.create_url, data=self.review_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)
        self.assertReviewExists(5, "Great class!")

    def test_list_reviews(self):
        Review.objects.create(user=self.user, yoga_class=self.yoga_class, rating=4, comments="Good class!")
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Good class!")

    def test_update_review(self):
        review = Review.objects.create(user=self.user, yoga_class=self.yoga_class, rating=3, comments="Okay class.")
        update_url = reverse("edit_review", kwargs={"pk": review.id})
        updated_data = {"yoga_class": self.yoga_class.id, "rating": 4, "comments": "Updated review"}

        response = self.client.post(update_url, data=updated_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)
        self.assertReviewExists(4, "Updated review")

    def test_delete_review(self):
        review = Review.objects.create(user=self.user, yoga_class=self.yoga_class, rating=3,
                                       comments="Temporary review")
        delete_url = reverse("delete_review", kwargs={"pk": review.id})

        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)
        self.assertFalse(Review.objects.filter(pk=review.id).exists(), "The review was not deleted.")

    def test_review_update_permission(self):
        other_user = get_user_model().objects.create_user(email="other@test.com", password="password123")
        review = Review.objects.create(user=other_user, yoga_class=self.yoga_class, rating=3, comments="Not yours.")
        update_url = reverse("edit_review", kwargs={"pk": review.id})

        response = self.client.post(update_url, data={"rating": 5, "comments": "Trying to update"})
        self.assertEqual(response.status_code, 404)
        self.assertFalse(
            Review.objects.filter(user=other_user, rating=5, comments="Trying to update").exists(),
            "Unauthorized update should not be allowed."
        )

    def test_review_delete_permission(self):
        other_user = get_user_model().objects.create_user(email="other@test.com", password="password123")
        review = Review.objects.create(user=other_user, yoga_class=self.yoga_class, rating=2, comments="Not yours.")
        delete_url = reverse("delete_review", kwargs={"pk": review.id})

        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            Review.objects.filter(pk=review.id).exists(),
            "Unauthorized deletion should not be allowed."
        )
