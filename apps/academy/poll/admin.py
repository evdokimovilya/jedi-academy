from django.contrib import admin
from .models import *

class QuestionInline(admin.TabularInline):
    model = Question

@admin.register(Poll)
class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        QuestionInline,
    ]


@admin.register(CandidatePoll)
class CandidatePoll(admin.ModelAdmin):
    list_display = ['candidate', 'question', 'correct']
