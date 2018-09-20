from django.shortcuts import render

from .models import Topic

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
