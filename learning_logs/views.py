from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    """학습 로그 홈페이지"""
    return render(request, 'learning_logs/index.html')

def topics(request):
    """주제를 표시한다."""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    """주제 하나와 연결된 모든 항목을 표시한다."""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

def new_topic(request):
    """새 주제 추가"""
    if request.method != 'POST':
        # 들어온 데이터가 없을 때는 새 폼을 만든다.
        form = TopicForm()
    else:
        # POST 데이터를 받아서 처리한다.
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

def new_entry(request, topic_id):
    """특정 주제에 관한 새 항목을 추가"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # 전송된 데이터가 없으므로 빈 폼을 만든다.
        form = EntryForm()
    else:
        # 받은 POST 데이터를 처리한다.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                        args=[topic_id]))

    context = {'topic':topic, 'form':form}
    return render(request, 'learning_logs/new_entry.html', context)

def edit_entry(request, entry_id):
    """기존 항목을 편집한다."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        # 첫 요청이므로 폼을 현재 텍스트로 채운다.
        form = EntryForm(instance=entry)
    else:
        # POST 데이터를 받았으므로 받은 데이터를 처리한다.
        form = EntryForm(instance=entry, data=request.POST)
        return HttpResponseRedirect(reverse('learning_logs:topic',
                                    args=[topic.id]))

    context = {'entry': entry, 'topic':topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
