from django.shortcuts import render

def index(request):
    """학습 로그 홈페이지"""
    return render(request, 'learning_logs/index.html')
