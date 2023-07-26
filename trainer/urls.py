from django.urls import path
from django.views.generic import TemplateView

from trainer import views

app_name = 'trainer'

urlpatterns = [
    path('', views.MainPageView.as_view(), name="main_page"),
    path('trainer/', views.WordTrainerView.as_view(), name='words_task'),
    path('trainer/fail', views.CheckAnswerView.as_view(), name='fail_page'),
]