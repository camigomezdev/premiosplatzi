import datetime
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from polls.models import Question

class QuestionModelTests(TestCase):

    def test_was_published_recently(self):
        """was_published_recently returns True for questions whose pub_date is recendly"""

        time = timezone.now()
        future_question = Question(question_text='Question test', pub_date=time)

        self.assertTrue(future_question.was_published_recently())

    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text='Question test', pub_date=time)

        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_with_past_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the past"""

        time = timezone.now() + datetime.timedelta(days=2)
        future_question = Question(question_text='Question test', pub_date=time)

        self.assertFalse(future_question.was_published_recently())

class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """If no question exists, an appropiate message is displayed"""
        response = self.client.get(reverse("polls:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_no_show_future_questions(self):
        """Questions no show future questions"""

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text='Question test', pub_date=time)
        future_question.save()

        response = self.client.get(reverse("polls:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_show_only_past_questions(self):
        """Questions only show past questions"""

        time_future = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text='Question test future', pub_date=time_future)
        future_question.save()

        time_past = timezone.now() - datetime.timedelta(days=30)
        past_question = Question(question_text='Question test past', pub_date=time_past)
        past_question.save()

        response = self.client.get(reverse("polls:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Question test past")
        self.assertNotContains(response, "Question test future")
        self.assertEqual(len(response.context["latest_question_list"]), 1)