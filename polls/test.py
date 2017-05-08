import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Question

def creation_question(question_text, days):
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionMethodTest(TestCase):
	def test_index_view_with_no_questions(self):
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'], [])
	def test_was_published_recently_with_future_question(self):
		"""
		was_published_recently() should return False for questions whose
		pub_date is in the future
		"""
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertEqual(future_question.was_published_recently(), False)
	def test_was_published_recently_with_old_question(self):
		"""
		was_published_recently() should return False for questinos whose
		pub_date is older than 1 days.
		"""
		time = timezone.now() - datetime.timedelta(days=30)
		old_question = Question(pub_date=time)
		self.assertEqual(old_question.was_published_recently(), False)
	def test_was_published_recently_with_recent_question(self):
		"""
		was_published_recently() should return False for questinos whose
		pub_date is with in the last day.
		"""
		time = timezone.now() - datetime.timedelta(hours=1)
		recent_question = Question(pub_date=time)
		self.assertEqual(recent_question.was_published_recently(), False)