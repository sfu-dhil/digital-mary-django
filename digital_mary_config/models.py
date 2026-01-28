from django.db import models
from django.utils.safestring import mark_safe
from solo.models import SingletonModel
from django_advance_thumbnail import AdvanceThumbnailField

# abstract Models

# Models (load order matters)
class AboutPage(SingletonModel):
    content = models.TextField()

    # relationships

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'digital_mary_config_about_page'
        verbose_name = 'About Page'

    def __str__(self):
        return 'About Page'

class TeamMember(models.Model):
    name = models.CharField()
    profile = models.TextField()
    image = models.ImageField(
        upload_to='images/',
        help_text=mark_safe('Please use <u><a href="https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types" target="_blank">standard web image types</a></u>. PNG, JPEG, and WebP are recommended.'),
        verbose_name='Profile Picture',
    )
    thumbnail = AdvanceThumbnailField(
        source_field='image',
        upload_to='thumbnails/',
        null=True,
        blank=True,
        size=(150, 150),
    )
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    # relationships
    about_page = models.ForeignKey(
        AboutPage,
        related_name='team_members',
        on_delete=models.CASCADE,
    )

    # one-to-many contributions via Contribution Model

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'digital_mary_config_team_member'
        ordering = ['order']

    def __str__(self):
        return self.name