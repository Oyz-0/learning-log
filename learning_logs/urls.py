"""Define URL patterns for learning_logs"""

from django.urls import path

from . import views

app_name = 'learning_logs'

urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page for the list of Topics
    path('topics/', views.topics, name='topics'),
    # Page for details of a single Topic
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # Page for creating a new Topic
    path('new_topic/', views.new_topic, name='new_topic'),
    # Page for adding a new Entry
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # Page for editing an Entry
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]