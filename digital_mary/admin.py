from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.postgres.fields import ArrayField
from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from tinymce.widgets import TinyMCE
from modeltrans_tabs.admin import TabbedLanguageMixin
from django.templatetags.static import static

from .marc_relators import MarcRelator
from .widgets import Select2ChoiceArrayWidget, Select2TagArrayWidget
from .models import Person, Category, Culture, InscriptionStyle, Language, \
    Location, Material, Subject, Technique, Item, Contribution, Image, RemoteImage

# Admin Panel Items
class AdminModelDefaults(ModelAdmin):
    # compressed_fields = True

    # all list displayed fields are display links
    def get_list_display_links(self, request, list_display):
        return self.list_display

    formfield_overrides = {
        models.TextField: {
            "widget": TinyMCE,
        },
    }

class AbstractTermModelDefaults(TabbedLanguageMixin, AdminModelDefaults):
    list_display = ['label', '_description']
    search_fields = ['label', 'description']
    ordering = ['label']

    def _description(self, obj):
        return mark_safe(obj.description) if obj.description else ''
    _description.short_description = 'Description'
    _description.admin_order_field = 'description'


@admin.register(Category)
class CategoryAdmin(AbstractTermModelDefaults):
    pass

@admin.register(Culture)
class CultureAdmin(AbstractTermModelDefaults):
    pass

@admin.register(InscriptionStyle)
class InscriptionStyleAdmin(AbstractTermModelDefaults):
    pass

@admin.register(Language)
class LanguageAdmin(AbstractTermModelDefaults):
    pass

@admin.register(Location)
class LocationAdmin(AbstractTermModelDefaults):
    list_display = ['label', 'country', '_description']
    search_fields = ['label', 'country', 'description']
    ordering = ['label']

    formfield_overrides = {
        ArrayField: {
            'widget': Select2TagArrayWidget(attrs={'data-placeholder': 'Click to add one or more alternate names'}),
        },
    }

@admin.register(Material)
class MaterialAdmin(AbstractTermModelDefaults):
    pass

@admin.register(Subject)
class SubjectAdmin(AbstractTermModelDefaults):
    formfield_overrides = {
        ArrayField: {
            'widget': Select2TagArrayWidget(attrs={'data-placeholder': 'Click to add one or more alternate names'}),
        },
    }

@admin.register(Technique)
class TechniqueAdmin(AbstractTermModelDefaults):
    pass

@admin.register(Person)
class PersonAdmin(ModelAdmin):
    fields = [
        ('fullname', 'citation_name'),
    ]
    list_display = ('fullname', 'citation_name')
    list_display_links = ('fullname', 'citation_name')
    ordering = ['fullname', 'citation_name']
    search_fields = ['fullname', 'citation_name']

class ContributionInline(TabularInline):
    fields = ['person', 'marc_relators', 'note']
    autocomplete_fields = ['person']
    model = Contribution
    ordering = ['id']
    extra = 0
    readonly_fields = ['note']
    formfield_overrides = {
        ArrayField: {
            'widget': Select2ChoiceArrayWidget(
                attrs={'data-placeholder': 'Click to select one or more roles'},
                choices=MarcRelator.choices,
            ),
        },
    }

    def note(self, obj):
        return mark_safe('See the list of <u><a href="https://www.loc.gov/marc/relators/relaterm.html" target="_blank">MARC Relators</a></u> for descriptions of each role')

class ImageInlineAdmin(TabbedLanguageMixin, StackedInline):
    fields = [
        ('_thumbnail_image_tag', 'image'),
        'name',
        'is_public',
        'description',
        'license',
    ]
    readonly_fields = ['_thumbnail_image_tag']
    ordering = ['id']
    model = Image
    extra = 0

    formfield_overrides = {
        models.TextField: {
            "widget": TinyMCE,
        },
    }

    def _thumbnail_image_tag(self, obj):
        return mark_safe(f'<img src="{obj.thumbnail.url}" style="max-width: 100%; max-height: 100px" />') if obj.thumbnail else ''
    _thumbnail_image_tag.short_description = 'Image Preview'

class RemoteImageInlineAdmin(TabbedLanguageMixin, StackedInline):
    fields = ['url', 'name', 'description']
    ordering = ['id']
    model = RemoteImage
    extra = 0

    formfield_overrides = {
        models.TextField: {
            "widget": TinyMCE,
        },
    }

@admin.register(Item)
class ItemAdmin(TabbedLanguageMixin, ModelAdmin):
    fields = [
        'name',
        'is_public',
        'categories',
        'description',
        'inscription',
        'translated_inscription',
        'languages',
        'inscription_style',
        'cultures',
        'culture_other',
        'display_date',
        'earliest_creation',
        'latest_creation',
        'provenance',
        'provenance_other',
        'findspot',
        'findspot_other',
        'dimensions',
        'materials',
        'techniques',
        'interpretations',
        'bibliographic_references',
        'location',
        'subjects',
    ]
    inlines = [
        ContributionInline,
        ImageInlineAdmin,
        RemoteImageInlineAdmin,
    ]

    list_filter = [
        'is_public',
        'categories', 'languages', 'inscription_style', 'cultures', 'provenance',
        'provenance', 'findspot', 'techniques', 'subjects',
    ]
    autocomplete_fields = [
        'categories', 'languages', 'inscription_style', 'cultures', 'provenance',
        'findspot', 'materials', 'techniques', 'subjects',
    ]
    list_display = ('name', 'is_public', '_display_date', '_image_count', '_display_image')
    list_display_links = ('name', 'is_public', '_display_date', '_display_image')
    ordering = ['name']
    search_fields = ['name', 'description']

    formfield_overrides = {
        models.TextField: {
            "widget": TinyMCE,
        },
    }

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('images', 'remote_images')

    def _display_date(self, obj):
        return obj.get_display_date()
    _display_date.short_description = 'Date'

    def _image_count(self, obj):
        return f'Public {obj.get_public_image_count()} / Private {obj.get_private_image_count()} / Remote {obj.remote_images.count()}'
    _image_count.short_description = '# Images'

    def _display_image(self, obj):
        # default image
        image = obj.get_first_public_image()
        url = image.thumbnail.url if image and image.image and image.thumbnail and image.thumbnail.url else static('images/no-img.svg')
        return mark_safe(f'<img src="{url}" style="max-width: 100%; max-height: 100px" />')
    _display_image.short_description = 'Display Image Preview'
