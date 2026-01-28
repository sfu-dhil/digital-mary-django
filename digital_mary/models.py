from django.db import models
from django_advance_thumbnail import AdvanceThumbnailField
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from modeltrans.fields import TranslationField
from html import unescape

from .marc_relators import MarcRelator

# abstract Models
class AbstractTerm(models.Model):
    label = models.CharField(db_index=True)
    description = models.TextField(null=True, blank=True)

    i18n = TranslationField(fields=('label', 'description'))

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return mark_safe(f'{self.label}')

# Models (load order matters)
class Category(AbstractTerm):
    # relationships

    # many-to-many items via Item Model

    class Meta:
        verbose_name_plural = 'categories'
        indexes = [
            GinIndex(fields=['i18n']),
        ]

class Culture(AbstractTerm):
    # relationships

    # many-to-many items via Item Model

    class Meta:
        indexes = [
            GinIndex(fields=['i18n']),
        ]

class InscriptionStyle(AbstractTerm):
    # relationships

    # one-to-many items via Item Model

    class Meta:
        db_table = 'digital_mary_inscription_style'
        indexes = [
            GinIndex(fields=['i18n']),
        ]

class Language(AbstractTerm):
    # relationships

    # many-to-many items via Item Model

    class Meta:
        indexes = [
            GinIndex(fields=['i18n']),
        ]

class Location(AbstractTerm):
    alternate_names = ArrayField(
        models.CharField(), default=list, blank=True
    )
    geonameid = models.IntegerField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    country = models.CharField(null=True, blank=True)

    i18n_field_params = {
        'fields': ('label', 'description'),
    }

    # relationships

    # one-to-many fondspot_items via Item Model
    # one-to-many provenance_items via Item Model

    class Meta:
        indexes = [
            GinIndex(fields=['i18n']),
        ]

class Material(AbstractTerm):
    # relationships

    # many-to-many items via Item Model

    class Meta:
        indexes = [
            GinIndex(fields=['i18n']),
        ]

class Subject(AbstractTerm):
    alternate_names = ArrayField(
        models.CharField(), default=list, blank=True
    )

    i18n_field_params = {
        'fields': ('label', 'description'),
    }

    # relationships

    # many-to-many items via Item Model

    class Meta:
        indexes = [
            GinIndex(fields=['i18n']),
        ]


class Technique(AbstractTerm):
    # relationships

    # many-to-many items via Item Model

    class Meta:
        indexes = [
            GinIndex(fields=['i18n']),
        ]

class Item(models.Model):
    class Periods(models.IntegerChoices):
        __empty__ = _('Unknown')
        C1 = 1, _('1st Century')
        C2 = 2, _('2nd Century')
        C3 = 3, _('3rd Century')
        C4 = 4, _('4th Century')
        C5 = 5, _('5th Century')
        C6 = 6, _('6th Century')
        C7 = 7, _('7th Century')
        C8 = 8, _('8th Century')
        C9 = 9, _('9th Century')
        C10 = 10, _('10th Century')
        C11 = 11, _('11th Century')
        C12 = 12, _('12th Century')
        C13 = 13, _('13th Century')
        C14 = 14, _('14th Century')
        C15 = 15, _('15th Century')
        C16 = 16, _('16th Century')
        C17 = 17, _('17th Century')
        C18 = 18, _('18th Century')
        C19 = 19, _('19th Century')
        C20 = 20, _('20th Century')
        C21 = 21, _('21st Century')

    name = models.CharField()
    is_public = models.BooleanField(db_index=True, default=True, verbose_name='Is Public?')
    description = models.TextField(null=True, blank=True)
    inscription = models.TextField(null=True, blank=True)
    translated_inscription = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    dimensions = models.TextField(null=True, blank=True)
    interpretations = models.TextField(null=True, blank=True)
    bibliographic_references = models.TextField(null=True, blank=True)
    display_date = models.CharField(null=True, blank=True)
    earliest_creation = models.IntegerField(choices=Periods.choices, null=True, blank=True)
    latest_creation = models.IntegerField(choices=Periods.choices, null=True, blank=True)

    culture_other = models.TextField(null=True, blank=True, verbose_name='culture (unknown)')
    findspot_other = models.TextField(null=True, blank=True, verbose_name='findspot (unknown)')
    provenance_other = models.TextField(null=True, blank=True, verbose_name='provenance (unknown)')

    i18n = TranslationField(fields=('name', 'description', 'translated_inscription', 'location', 'dimensions', 'interpretations', 'bibliographic_references', 'culture_other', 'findspot_other', 'provenance_other'))

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    search_vector = models.GeneratedField(
        expression=SearchVector('name', config='english', weight='A') +
            SearchVector('i18n__name_ar', config='arabic', weight='A') +
            SearchVector('description', config='english', weight='B') +
            SearchVector('i18n__description_ar', config='arabic', weight='B') +
            SearchVector('translated_inscription', config='english', weight='B') +
            SearchVector('i18n__translated_inscription_ar', config='arabic', weight='B') +
            SearchVector('inscription', config='simple', weight='C'),
        output_field=SearchVectorField(),
        db_persist=True,
    )

    # relationships
    categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name='items',
    )
    cultures = models.ManyToManyField(
        Culture,
        blank=True,
        related_name='items',
    )
    inscription_style = models.ForeignKey(
        InscriptionStyle,
        null=True,
        blank=True,
        related_name='items',
        on_delete=models.CASCADE,
    )
    languages = models.ManyToManyField(
        Language,
        blank=True,
        related_name='items',
    )
    findspot = models.ForeignKey(
        Location,
        null=True,
        blank=True,
        related_name='fondspot_items',
        on_delete=models.CASCADE,
    )
    provenance = models.ForeignKey(
        Location,
        null=True,
        blank=True,
        related_name='provenace_items',
        on_delete=models.CASCADE,
    )
    techniques = models.ManyToManyField(
        Technique,
        blank=True,
        related_name='items',
    )
    materials = models.ManyToManyField(
        Material,
        blank=True,
        related_name='items',
    )
    subjects = models.ManyToManyField(
        Subject,
        blank=True,
        related_name='items',
    )

    # one-to-many images via Image Model
    # one-to-many remote_images via RemoteImage Model
    # one-to-many contributions via Contribution Model

    class Meta:
        indexes = [
            GinIndex(fields=['i18n']),
            GinIndex(fields=['search_vector']),
        ]

    def __str__(self):
        return self.name

    def get_display_date(self):
        if self.display_date:
            return self.display_date
        return self.get_display_periods()

    def get_display_periods(self):
        if self.earliest_creation and self.latest_creation:
            return f'{self.Periods(self.earliest_creation).label} - {self.Periods(self.latest_creation).label}'
        elif self.earliest_creation:
            return self.Periods(self.earliest_creation).label
        elif self.latest_creation:
            return self.Periods(self.latest_creation).label
        return self.Periods.__empty__

    def get_citation_authors(self):
        return [
            f'{contribution.person.citation_name}.' for contribution in self.contributions.all() if MarcRelator.AUT in contribution.marc_relators
        ]

    def get_public_images(self):
        return self.images.filter(is_public=True).all()

    def get_first_public_image(self):
        return self.images.filter(is_public=True).first()

    def get_public_image_count(self):
        return self.images.filter(is_public=True).count()

    def get_private_images(self):
        return self.images.filter(is_public=False).all()

    def get_private_image_count(self):
        return self.images.filter(is_public=False).count()


class Image(models.Model):
    name = models.CharField(verbose_name='Image Name', null=True, blank=True)
    is_public = models.BooleanField(db_index=True, default=False, verbose_name='Is Public?')
    image = models.ImageField(
        upload_to='images/',
        width_field='image_width',
        height_field='image_height',
        help_text=mark_safe('Please use <u><a href="https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types" target="_blank">standard web image types</a></u>. PNG, JPEG, and WebP are recommended.'),
    )
    image_width = models.IntegerField(null=True, blank=True)
    image_height = models.IntegerField(null=True, blank=True)
    thumbnail = AdvanceThumbnailField(
        source_field='image',
        upload_to='thumbnails/',
        null=True,
        blank=True,
        size=(450, 350),
    )
    description = models.TextField(null=True, blank=True)
    license = models.TextField(null=True, blank=True)

    i18n = TranslationField(fields=('name', 'description', 'license'))

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # relationships
    item = models.ForeignKey(
        Item,
        related_name='images',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

class RemoteImage(models.Model):
    name = models.CharField(verbose_name='Image Name', null=True, blank=True)
    url = models.URLField(blank=False)
    description = models.TextField(null=True, blank=True)

    i18n = TranslationField(fields=('name', 'description'))

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # relationships
    item = models.ForeignKey(
        Item,
        related_name='remote_images',
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'digital_mary_remote_image'

    def __str__(self):
        return self.name

class Person(models.Model):
    fullname = models.CharField(db_index=True)
    citation_name = models.CharField(db_index=True, null=True, blank=True)

    # relationships

    # one-to-many contributions via Contribution Model

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'people'

    def __str__(self):
        return self.citation_name if self.citation_name else self.fullname

class Contribution(models.Model):
    # relationships
    item = models.ForeignKey(
        Item,
        related_name='contributions',
        on_delete=models.CASCADE,
    )
    person = models.ForeignKey(
        Person,
        related_name='contributions',
        on_delete=models.CASCADE
    )
    marc_relators = ArrayField(models.CharField(choices=MarcRelator.choices), default=list, verbose_name='roles')

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['person__citation_name']

    def __str__(self):
        return f'{self.person if self.person else 'N/A'} ({self.get_roles()})'

    def get_roles(self):
        return ', '.join([MarcRelator(marc_relator).label for marc_relator in self.marc_relators])