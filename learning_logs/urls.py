"""learning_logs의 URL 패턴을 정의한다."""

from django.urls import re_path

from . import views

urlpatterns = [
    #홈페이지
    re_path(r'^$', views.index, name='index'),

    # 주제를 모두 표시한다.
    re_path(r'^topics/$', views.topics, name='topics'),
    # 주제 하나에 대한 세부사항 페이지
    re_path(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),

    # 새 주제를 추가하는 페이지
    re_path(r'^new_topic/$', views.new_topic, name = 'new_topic'),
    # 새 항목을 추가하는 페이지
    re_path(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry,
     name = 'new_entry'),
     # 항목을 편집하는 페이지
     re_path(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry,
     name = 'edit_entry'),
]
