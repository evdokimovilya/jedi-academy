from .views import *
from django.urls import path, include

urlpatterns = [
	path('', index),
    path('candidate/new/', new_candidate),
    path('jedis/', jedis),
    path('jedis/all_jedis/', all_jedis),
    path('jedis/home/<int:jedi_id>/', jedi_home),
    path('candidates/home/<int:candidate_id>/', candidate_home),
    path('api/get_candidates/', get_candidates),
    path('api/get_padawans/', get_padawans),
    path('api/accept_candidate/', accept_candidate),
    path('api/delete_padawan/', delete_padawan)
]



