"""
URL Configuration para Core App
"""

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('topic/<str:code>/', views.TopicDetailView.as_view(), name='topic_detail'),
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category_list'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('course/', views.CourseView.as_view(), name='course_mode'),
]
