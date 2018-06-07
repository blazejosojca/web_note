from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


# only logged owner can CRUD content,
# for others 404 will be displayed
def check_topic_owner(request, topic):
    if topic.owner != request.user:
        raise Http404


def index(request):
    return render(request, 'notes/index.html')


def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    ctx = {'topics': topics}
    return render(request, 'notes/topics.html', ctx)

#
# def error_404(request):
#     data = {}
#     return render(request, 'notes/error_404.html', data)
#
#
# def error_500(request):
#     data = {}
#     return render(request, 'notes/error_500.html', data)


@login_required
def topic(request, pk):
    topic = Topic.objects.get(pk = pk)
    check_topic_owner(request, topic)
    # displays topic owned by user or returns 404 page
    entries = topic.entry_set.order_by('-entry_date_added')
    ctx = {'topic': topic, 'entries': entries}
    return render(request, 'notes/topic.html', ctx)


@login_required
def new_topic(request):
    if request.method == 'GET':
        form = TopicForm()
    elif request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('notes:topics'))

    ctx = {'form': form}
    return render(request, 'notes/new_topic.html', ctx)


@login_required
def edit_topic(request, topic_pk):
    topic = Topic.objects.get(pk=topic_pk)
    check_topic_owner(request, topic)
    if request.method != 'POST':
        form = TopicForm(instance=topic)
    elif request.method == 'POST':
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('notes:topic', args=[topic.id])
            )
    ctx = {'topic': topic, 'form': form}
    return render(request, 'notes/edit_topic.html', ctx)

@login_required
def delete_topic(request, topic_pk):
    topic = get_object_or_404(Topic, pk=topic_pk)
    check_topic_owner(request, topic)
    if request.method == 'POST':
        topic.delete()
        return HttpResponseRedirect("notes:index")
    ctx = {'topic': topic}
    return render(request, 'notes/delete_topic_confirm.html', ctx)


@login_required
def new_entry(request, topic_pk):
    topic = Topic.objects.get(pk=topic_pk)
    check_topic_owner(request, topic)
    if request.method != 'POST':
        form = EntryForm()
    elif request.method == 'POST':
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(
                reverse('notes:topic', args=[topic.id]))
    ctx = {'topic': topic, 'form': form}
    return render(request, 'notes/new_entry.html', ctx)


@login_required
def edit_entry(request, entry_pk):
    entry = Entry.objects.get(pk=entry_pk)
    topic = entry.topic
    check_topic_owner(request, topic)
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    elif request.method == 'POST':
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('notes:topic', args=[topic.id])
            )
    ctx = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'notes/edit_entry_confirm.html', ctx)


@login_required
def delete_entry(request, entry_pk):
    entry = get_object_or_404(Entry, pk=entry_pk)
    topic = entry.topic
    check_topic_owner(request, topic)
    if request.method == 'POST':
        entry.delete()
        return HttpResponseRedirect("notes:index")
    ctx = {'entry': entry, 'topic': topic}
    return render(request, 'notes/delete_entry_confirm.html', ctx)
