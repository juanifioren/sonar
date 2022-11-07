from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from django.http import JsonResponse
from django.utils.timezone import now, timedelta
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView

from sonar.models import ActivityLog, Post, User


class DashboardView(TemplateView):

    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_posts'] = Post.objects.all().count()
        context['total_users'] = User.objects.all().count()

        top_posts_views = (
            Post.objects
            .filter(activity_logs__interaction_type=ActivityLog.VIEW)
            .values('id')
            .annotate(total_views=Count('id'))
            .order_by('-total_views')[:5]
        )
        context['top_viewed_posts'] = [(Post.objects.get(id=e['id']), e['total_views']) for e in top_posts_views]

        top_posts_likes = (
            Post.objects
            .filter(activity_logs__interaction_type=ActivityLog.LIKE)
            .values('id')
            .annotate(total_likes=Count('id'))
            .order_by('-total_likes')[:5]
        )
        context['top_liked_posts'] = [(Post.objects.get(id=e['id']), e['total_likes']) for e in top_posts_likes]

        return context


@method_decorator(login_required, name='dispatch')
class PostsView(ListView):

    context_object_name = 'posts'
    paginate_by = 15
    template_name = 'posts.html'

    def get_queryset(self):
        return Post.objects.order_by('-date_created', '-id').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # For paginated posts, get those ids of which were liked by the user.
        context['posts_liked'] = list(self.object_list.filter(
            activity_logs__user=self.request.user,
            activity_logs__interaction_type=ActivityLog.LIKE)\
            .values_list('id', flat=True))
        return context


@method_decorator(login_required, name='dispatch')
class PostDetailView(DetailView):

    model = Post
    context_object_name = 'post'
    template_name = 'post_detail.html'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()

        # Create a view count log only every 3 hours, to prevent spamming.
        three_hours_ago = now() - timedelta(hours=3)
        query_kwargs = {
            'post': post,
            'user': request.user,
            'interaction_type': ActivityLog.VIEW,
        }
        if not ActivityLog.objects.filter(
            date_created__gte=three_hours_ago, **query_kwargs).exists():
            ActivityLog.objects.create(**query_kwargs)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
