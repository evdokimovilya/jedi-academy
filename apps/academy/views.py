from django.shortcuts import render, redirect
from .models import *
from apps.academy.poll.models import CandidatePoll
from django.conf import settings
from django.http import JsonResponse, Http404
from django.db.models import Count
from .forms import CandidateForm
from django.core.mail import send_mail
from django.conf import settings

def index(request):
	# main page

	return render(request, 'academy/index.html')

def new_candidate(request):
	# add new candidate

	# new candidate form
	if request.method == 'GET':
		planets = Planet.objects.all()
		context = {'planets': planets}

		return render(request, 'academy/new_candidate.html', context)

	else:
		# add info
		form = CandidateForm(request.POST)
		if form.is_valid():
			candidate = form.save()
			return redirect(settings.HOST +'poll/new/%d/' % candidate.pk) # redirect to poll

def jedis(request):
	"""Form with jedis selection"""
	jedis = Jedi.objects.all()

	return render(request, 'academy/jedis.html', {'jedis': jedis})


def all_jedis(request):
	"""List of all jedis"""

	# filter
	if 'filter' in request.GET.keys():
		filter = request.GET.get('filter')
		if filter == 'top':
			jedis = Jedi.objects.annotate(count_pad=Count('jedi_candidates')).filter(count_pad__gte=1)
	else:
		jedis = Jedi.objects.all()

	return render(request, 'academy/all_jedis.html', {'jedis': jedis})


def jedi_home(request, jedi_id):
	"""Jedi home - candidates and padawans"""
	if Jedi.objects.filter(pk=jedi_id).exists():
		jedi = Jedi.objects.get(pk=jedi_id)
		jedi_candidates = jedi.get_candidates()

		return render(request, 'academy/jedi_home.html', {'jedi': jedi, 'candidates': jedi_candidates})

	raise Http404

def candidate_home(request, candidate_id):
	"""Candidate home - test results, info"""

	if Candidate.objects.filter(pk=candidate_id).exists():
		candidate = Candidate.objects.get(pk=candidate_id)
		answers = CandidatePoll.objects.filter(candidate=candidate)

		return render(request, 'academy/candidate_home.html', {'candidate': candidate,'answers': answers })

	raise Http404


# API section for vue.js on jedi home page)
def get_candidates(request):
	"""get all jedi candidates"""

	jedi_pk = int(request.GET.get('jedi_pk'))
	jedi = Jedi.objects.get(pk=jedi_pk)
	jedi_padawans = len(jedi.get_padawans()) # for checking padawans limit
	candidates = list(jedi.get_candidates().values())

	return JsonResponse({'candidates': candidates,  'jedi_padawans': jedi_padawans})


def get_padawans(request):
	"""Get all jedi padawans"""

	jedi_pk = int(request.GET.get('jedi_pk'))
	jedi = Jedi.objects.get(pk=jedi_pk)
	jedi_padawans = len(jedi.get_padawans())
	padawans = list(jedi.get_padawans().values())

	return JsonResponse({'padawans': padawans, 'jedi_padawans': jedi_padawans})


def accept_candidate(request):
	"""Accept candidate to padawans"""
	get_r = request.GET.copy()
	jedi_pk = get_r.get('jedi_pk')
	candidate_pk = get_r.get('candidate_pk')

	jedi = Jedi.objects.get(pk=jedi_pk)
	padawans = jedi.get_padawans()

	# limit checking
	if len(padawans) < 3:
		candidate = Candidate.objects.get(pk=candidate_pk)
		candidate.jedi = jedi
		candidate.save()

		if settings.SEND_EMAIL:
			send_mail(
				'You was accepted to padawans',
				'Congratulations!',
				'from@example.com',
				[candidate.email],
				fail_silently=False,
			)

			return JsonResponse({})
	else:
		return JsonResponse({})

def delete_padawan(request):
	"""Delete padawan from jedi"""
	get_r = request.GET.copy()
	padawan_pk = get_r.get('padawan_pk')

	candidate = Candidate.objects.get(pk=padawan_pk)
	candidate.jedi = None
	candidate.save()

	return JsonResponse({})
