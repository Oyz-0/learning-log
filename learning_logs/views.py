from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    """The homepage for Learning Log."""
    return render(request, 'learning_logs/index.xhtml')

@login_required
def topics(request):
    """The Topics page for Learning Log."""
    topics = Topic.objects.filter(owner=request.user).order_by('date')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.xhtml', context)

@login_required
def topic(request, topic_id):
    """Show a single Topic and all its Entries"""
    topic = Topic.objects.get(id=topic_id)
    # Make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.xhtml', context)

@login_required
def new_topic(request):
    """Create a new Topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
    if form.is_valid():
        new_topic = form.save(commit=False)
        new_topic.owner = request.user
        new_topic.save()
        return redirect('learning_logs:topics')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.xhtml', context)

@login_required
def new_entry(request, topic_id):
    """Create a new Entry."""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
    if form.is_valid():
        new_entry = form.save(commit=False)
        new_entry.topic = topic
        new_entry.save()
        return redirect('learning_logs:topic', topic_id=topic_id)
    
    # Display a blank or invalid Entry.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.xhtml', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing Entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('learning_logs:topic', topic_id=topic.id)
    
    context = {'entry': entry, 'form': form, 'topic': topic}
    return render(request, 'learning_logs/edit_entry.xhtml', context)
            