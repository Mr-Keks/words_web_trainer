from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib import messages

import json
import random

from .forms import WordForm


class MainPageView(TemplateView):
    template_name = 'main.html'


def set_temp_data(request, word, translation):
    request.session['word'] = word
    request.session['translation'] = translation


def get_temp_data(request):
    translation = request.session.get('translation')
    return translation


def get_temp_word_data(request):
    return request.session.get('word')


def load_words_and_translations():
    with open('trainer/static/translate_word_list.json') as file:
        return json.load(file)


WORDS_AND_TRANSLATIONS = load_words_and_translations()


class WordTrainerView(FormView):
    template_name = 'trainer.html'
    form_class = WordForm
    success_url = '/trainer/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        words_list = list(WORDS_AND_TRANSLATIONS.keys())
        random_word = random.choice(words_list)

        word_form = WordForm(initial={'word': '', 'target': random_word})
        context["form"] = word_form
        context["target"] = random_word
        set_temp_data(self.request, random_word, WORDS_AND_TRANSLATIONS[random_word])
        return context

    def form_valid(self, form):
        user_answer = form.cleaned_data['word']
        if user_answer in get_temp_data(self.request):
            messages.add_message(self.request, messages.SUCCESS, 'Good job!')
            return super().form_valid(form)
        else:
            messages.add_message(self.request, messages.WARNING, 'this is not correct(')
            return render(self.request, 'fail.html', context={
                'word': get_temp_word_data(self.request),
                'user_answer': user_answer,
                'translate': get_temp_data(self.request)
            })


class CheckAnswerView(TemplateView):
    template_name = 'fail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context = {
            'word': get_temp_word_data(self.request),
            'user_answer' :  '',
            'translate': get_temp_data(self.request)
        }
        
        return context
    
    
        