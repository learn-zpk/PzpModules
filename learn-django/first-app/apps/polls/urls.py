from django.urls import path

from . import views
from .models import Question, Choice
from django.contrib import admin

from .views import IndexView, DetailView, ResultsView

#admin.site.register(Question)
admin.site.register(Choice)

app_name = 'polls'
urlpatterns = [
    # path('', views.index, name='index'),
    # path('<int:question_id>', views.detail, name='detail'),
    # path('<int:question_id>/results/', views.results, name='results'),
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>', DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote')
]
