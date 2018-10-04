from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm

def logout_view(request):
    """사용자 로그아웃"""
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))

def register(request):
    """새 사용자를 등록한다."""
    if request.method != 'POST':
        # 빈 등록 폼을 표시한다.
        form = UserCreationForm()
    else:
        # 전송받은 폼을 처리한다.
        form = UserCreationForm(data = request.POST)

        if form.is_valid():
            new_user = form.save()
            # 사용자를 로그인시키고 홈페이지로 리다이렉트한다.
            authenticated_user = authenticate(username=new_user.username,
                password=request.POST['password1'])
            login(request, quthenticated_user)
            return HttpResponseRedirect(reverse('learning_logs:index'))

    context = {'form': form}
    return render(request, 'users/register.html', context)
