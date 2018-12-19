from django.shortcuts import render
from django.http import JsonResponse, Http404
from .models import *
from apps.academy.models import *



def poll(request, candidate_id):
	""""new poll"""

	if Candidate.objects.filter(id=candidate_id).exists():
		candidate = Candidate.objects.get(id=candidate_id)

		if not CandidatePoll.objects.filter(candidate=candidate):

			if not candidate.jedi:
				poll = Poll.objects.all()[0]

				return render(request, 'poll/new_poll.html', {'candidate_pk':candidate_id, 'poll_pk': poll.pk} )

	raise Http404

def question(request):
	"""return next question"""

	# poll_pk - for the future
	poll_pk = request.GET.get('poll_pk')
	last_question = int(request.GET.get('last_question'))

	# send text question to vue.js
	if Poll.objects.filter(pk=poll_pk).exists():
		poll = Poll.objects.get(pk=poll_pk)
		questions_number = len(poll.poll_questions.all())

		if questions_number > last_question:
			question = poll.poll_questions.all().order_by('number')[last_question]

			return JsonResponse({'text':question.text, 'pk': question.pk, 'poll_pk': question.poll.pk, 'end': False})
		else:
			# if questions is over
			return JsonResponse({'end': True})

	raise Http404


def answer(request):
	""""save user answer"""
	r_get = request.GET.copy()
	question_pk = int(r_get.get('question_pk'))
	candidate_pk = int(r_get.get('candidate_pk'))
	answer = int(r_get.get('poll_answer'))

	question = Question.objects.get(pk=question_pk)
	candidate = Candidate.objects.get(pk=candidate_pk)

	if question.correct and answer == 1 or not question.correct and answer == 0:
		true_answer = True
	else:
		true_answer = False

	candidate_poll = CandidatePoll.objects.get_or_create(
		candidate=candidate, question=question, correct=true_answer)

	return JsonResponse({})

