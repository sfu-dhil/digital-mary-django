from django.db import models

from digital_mary.models import Item

# abstract Models

# Models (load order matters)
class Challenge(models.Model):
    fullname = models.CharField()
    email = models.EmailField()
    message = models.TextField()
    archive = models.BooleanField(default=False, verbose_name='archived?')

    # relationships
    item = models.ForeignKey(
        Item,
        related_name='challenges',
        on_delete=models.CASCADE,
    )

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.fullname} messaged on {self.created.strftime("%Y-%m-%d %H:%M")}'
