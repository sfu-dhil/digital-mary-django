from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.http import urlencode
from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from django.templatetags.static import static
from django.shortcuts import redirect

from digital_mary.models import Item
from .models import Challenge



# Admin Panel Items
@admin.register(Challenge)
class ChallengeAdmin(ModelAdmin):
    list_filter = ['archive', 'item', 'fullname', 'email']
    list_display = ('item', 'created', 'fullname',  'email', 'message')
    list_display_links = ('created', 'fullname',  'email', 'message')
    ordering = ['-created']
    search_fields = ['fullname', 'email', 'message']
    autocomplete_fields = ['item']
    actions = ['archive_challenges', 'unarchive_challenges']

    readonly_fields = ['item', 'fullname', 'email', 'message']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('item')

    def has_change_permission(self, request, obj=None):
        return True
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return True

    @admin.action(description="Archive selected challenges")
    def archive_challenges(self, request, queryset):
        queryset.update(archive=True)

    @admin.action(description="Unarchive selected challenges")
    def unarchive_challenges(self, request, queryset):
        queryset.update(archive=False)