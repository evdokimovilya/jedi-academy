from django.db import models
from apps.academy.models import *

class Poll(models.Model):
	name = models.CharField(max_length=255, name='name')
	oder_code = models.IntegerField(name='order_code')

	def __str__(self):
		return self.name

class Question(models.Model):
	text = models.TextField(name='text')
	poll = models.ForeignKey(Poll, related_name='poll_questions', on_delete=models.CASCADE)
	correct = models.BooleanField(name='correct', default=False, help_text='True - question is correct')
	number = models.IntegerField(name='number')

	def __str__(self):
		return str(self.text)

class CandidatePoll(models.Model):
	candidate = models.ForeignKey(Candidate, related_name='candidate_polls', on_delete=models.CASCADE)
	question = models.ForeignKey(Question, related_name='question_candidate_polls', on_delete=models.CASCADE)
	correct = models.BooleanField(name='correct', default=False, help_text="candidate's answer was correct")

	def __str__(self):
		return self.candidate.email


