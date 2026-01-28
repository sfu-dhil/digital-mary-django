from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from solo.admin import SingletonModelAdmin
from django.contrib.admin import ModelAdmin
from tinymce.widgets import TinyMCE
from adminsortable2.admin import SortableTabularInline, SortableAdminBase
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.utils.translation import gettext as _
from django.utils.encoding import force_str
from django.contrib import messages

from .models import AboutPage, TeamMember


class TeamMemberInline(SortableTabularInline):
    fields = ['_thumbnail_image_tag', 'image', 'name', 'profile', 'order']
    readonly_fields = ['_thumbnail_image_tag']
    model = TeamMember
    extra = 0

    formfield_overrides = {
        models.TextField: {
            "widget": TinyMCE,
        },
    }

    def _thumbnail_image_tag(self, obj):
        return mark_safe(f'<img src="{obj.thumbnail.url}" style="max-width: 150px; max-height: 150px" />') if obj.thumbnail else ''
    _thumbnail_image_tag.short_description = 'Profile Thumbnail Preview'


# Admin Panel Items
@admin.register(AboutPage)
class AboutPageAdmin(SortableAdminBase, SingletonModelAdmin):
    formfield_overrides = {
        models.TextField: {
            "widget": TinyMCE,
        },
    }

    inlines = [
        TeamMemberInline,
    ]

    # Fix user message success vs info 
    def response_change(self, request, obj):
        msg = _("{obj} was changed successfully.").format(obj=force_str(obj))
        if "_continue" in request.POST:
            self.message_user(request, msg + " " + _("You may edit it again below."), messages.SUCCESS)
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg, messages.SUCCESS)
            return HttpResponseRedirect("../../")