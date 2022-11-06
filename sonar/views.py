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
        return Post.objects.order_by('-date_created', '-id').all()
