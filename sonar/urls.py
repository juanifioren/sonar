from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from sonar.views import PostsView, PostLikeView


urlpatterns = [
    path('', PostsView.as_view(), name='posts'),
    path('admin/', admin.site.urls),
    path('post-like/', PostLikeView.as_view(), name='post-like'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]
