from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),

    # my_blog url
    re_path(r'', include(('learning_logs.urls', 'learning_logs'),
        namespace='learning_logs')),

    # users url
    re_path(r'^users/', include(('users.urls', 'users'), namespace=None))
]
