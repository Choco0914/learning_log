from django.contrib import admin
from django.urls import path, re_path, include

app_name = 'learning_logs'

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'', include(('learning_logs.urls', 'learning_logs'),
        namespace='learning_logs')),
]
