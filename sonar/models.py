from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Post(models.Model):

    image_src = models.URLField(null=True, blank=True, max_length=250)
    title = models.CharField(null=True, blank=True, max_length=250)
    description = models.TextField(null=True, blank=True, help_text=_('HTML supported.'))  # noqa
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        default_permissions = ()
        ordering = ['date_created', 'id']
        verbose_name = _('Activity Log')
        verbose_name_plural = _('Activity Logs')

    def __str__(self):
        return self.title

    def __repr__(self):
        return '<Post {} {}>'.format(self.user.username, self.get_interaction_type_display())  # noqa

    @property
    def slug(self):
        return slugify(self.title)


class ActivityLog(models.Model):

    LIKE = 'LIKE'
    VIEW = 'VIEW'
    INTERACTION_CHOICES = [
        (LIKE, _('Like')),
        (VIEW, _('View')),
    ]

    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='activity_logs')  # noqa
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activity_logs')  # noqa
    interaction_type = models.CharField(max_length=10, choices=INTERACTION_CHOICES)
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        default_permissions = ()
        ordering = ['date_created', 'id']
        verbose_name = _('Activity Log')
        verbose_name_plural = _('Activity Logs')

    def __str__(self):
        return self.get_interaction_type_display()

    def __repr__(self):
        return '<ActivityLog {} {}>'.format(self.user.username, self.get_interaction_type_display())  # noqa
