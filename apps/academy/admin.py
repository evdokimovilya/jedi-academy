from django.contrib import admin
from .models import *


@admin.register(Jedi)
class DjedayAdmin(admin.ModelAdmin):
	pass


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
	pass


@admin.register(Planet)
class PlanetAdmin(admin.ModelAdmin):
	pass
