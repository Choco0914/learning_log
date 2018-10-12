from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse


from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    """학습 로그 홈페이지"""
    return render(request, 'learning_logs/index.html')

# this should really be a method on a custom ModelManager
def _get_topics_for_user(user):
    " returns a queryset of topics the user can access "
    q = Q(public=True)
    # if django < 1.10 you want "user.is_authenticated()" (with parens)
    if user.is_authenticated:
       # adds user's own private topics to the query
       q = q | Q(public=False, owner=user)

    return Topic.objects.filter(q)

def topics(request):
    """주제를 표현한다"""
    topics = _get_topics_for_user(request.user).order_by('date_added')
    form = TopicForm()
    context = {'topics': topics, 'form': form}
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    topics = _get_topics_for_user(request.user)
    topic = get_object_or_404(topics, id=topic_id)
    form = TopicForm()
    # here we're passing the filtered queryset, so
    # if the topic "topic_id" is private and the user is either
    # anonymous or not the topic owner, it will raise a 404
    if topic.owner == request.user:
            entries = topic.entry_set.order_by('-date_added')
            context = {'topic': topic, 'entries': entries, 'form': form}
            return render(request, 'learning_logs/topic.html', context)
    else:
        entries = topic.entry_set.order_by('-date_added')
        context = {'topic': topic, 'entries': entries, 'form': form}
    return render(request, 'learning_logs/public_topic.html', context)

def read_entry(request, entry_id):
    "내용을 자세히 보여준는 페이지를 반환한다."
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic

    context = {'entry': entry, 'topic':topic}
    return render(request, 'learning_logs/read_entry.html', context)

@login_required
def new_topic(request):
    """새 주제 추가"""
    if request.method != 'POST':
        # 들어온 데이터가 없을 때는 새 폼을 만든다.
        form = TopicForm()
    else:
        # POST 데이터를 받아서 처리한다.
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """특정 주제에 관한 새 항목을 추가"""
    topic = get_object_or_404(Topic, id=topic_id)
    check_user = check_topic_owner(request, topic)

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

@login_required
def edit_entry(request, entry_id):
    """기존 항목을 편집한다."""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    check_user = check_topic_owner(request, topic)

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

@login_required
def topics_remove(request, topic_id):
    """주제를 삭제한다."""
    topic = get_object_or_404(Topic, id=topic_id)
    check_user = check_topic_owner(request, topic)

    topic.delete()
    return HttpResponseRedirect(reverse('learning_logs:topics'))

@login_required
def entries_remove(request, entry_id):
    """내용을 삭제한다."""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    topic_id = entry.topic.id
    check_user = check_topic_owner(request, topic)

    entry.delete()
    return HttpResponseRedirect(reverse('learning_logs:topic',
                                args=[topic_id]))

def check_topic_owner(request, topic):
    """현재 유저가 올바른 유저인지 체크한다"""
    if topic.owner != request.user:
        raise Http404
