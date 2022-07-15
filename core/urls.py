from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index),
    path('spider/', views.spider, name='spider'),
    path('analysis/', views.analysis, name='analysis'),
    path('word/', views.word_generate),
    path('detail/', views.detail, name='detail')
]
