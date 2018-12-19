from .views import *
from django.urls import path, include

urlpatterns = [
	path('poll/new/<int:candidate_id>/', poll),
	path('poll/question/', question),
	path('poll/answer/', answer),
]



