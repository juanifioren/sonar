from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from sonar.models import Post


@method_decorator(login_required, name='dispatch')
class PostsView(ListView):

    context_object_name = 'posts'
    paginate_by = 12
    template_name = 'posts.html'

    def get_queryset(self):
        queryset = Post.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
