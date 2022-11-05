from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

from sonar import models


admin.site.site_header = 'Sonar Admin'
admin.site.site_title = admin.site.site_header


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ('short_title', 'date_created')
    list_filter = ('date_created',)
    search_fields = ('title',)

    def short_title(self, instance):
        return truncatechars(instance.title, 60)
    short_title.short_description = 'Title'


@admin.register(models.ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):

    list_display = ('short_title', 'date_created')
    list_filter = ('date_created',)
    search_fields = ('title',)

    def short_title(self, instance):
        return truncatechars(instance.title, 60)
    short_title.short_description = 'Title'
