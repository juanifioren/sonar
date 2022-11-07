from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from sonar.views import PostsView, PostDetailView, PostLikeView


urlpatterns = [
    path('', PostsView.as_view(), name='posts'),
    path('admin/', admin.site.urls),
    path('post/<pk>/<slug>/', PostDetailView.as_view(), name='post-detail'),
    path('post/like/', PostLikeView.as_view(), name='post-like'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]
