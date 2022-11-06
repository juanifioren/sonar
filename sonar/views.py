from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView

from sonar.models import ActivityLog, Post


@method_decorator(login_required, name='dispatch')
class PostsView(ListView):

    context_object_name = 'posts'
    paginate_by = 12
    template_name = 'posts.html'

    def get_queryset(self):
        return Post.objects.order_by('-date_created', '-id').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts_liked'] = list(self.object_list.filter(
            activity_logs__user=self.request.user,
            activity_logs__interaction_type=ActivityLog.LIKE)\
            .values_list('id', flat=True))
        return context


@method_decorator(login_required, name='dispatch')
class PostLikeView(View):

    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise JsonResponse(status=400)

        query_kwargs = {
            'post': post,
            'user': request.user,
            'interaction_type': ActivityLog.LIKE,
        }

        # Try delete if exists, if not then create it.
        try:
            ActivityLog.objects.get(**query_kwargs).delete()
        except ActivityLog.DoesNotExist:
            ActivityLog.objects.create(**query_kwargs)

        return JsonResponse({})
