from django.shortcuts import render, redirect

from .forms import TopicForm, EntryForm
from .models import Topic, Entry

# Create your views here.
def index(request):
    return render(request, 'learning_logs/index.html')


def topics(request):
    """Show all topics."""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    """Show a topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)
    entries = Entry.objects.filter(topic_id=topic.id)
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    myvar = "Hello World"

    if request.method != 'POST':    # bu bir GET isteğidir
        form = EntryForm()
    else:                           # POST isteği
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    context = {'form': form, 'topic': topic, 'myvar': myvar}
    return render(request, 'learning_logs/new_entry.html', context)


def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)

    if request.method != 'POST':   # Burası GET
        form = EntryForm(instance=entry)
    else:                          # Burası POST
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=entry.topic.id)

    context = {'entry': entry, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


def delete_entry(request, entry_id):
    """Delete an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    entry.delete()
    return redirect('learning_logs:topic', topic_id=topic.id)


def delete_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    topic.delete()
    return redirect('learning_logs:topics')
