from django.db import models
from django.conf import settings
from django.db.models import Q


class Series(models.Model):
    """Model representing a TV series in the watchlist."""

    PROVIDER_CHOICES = [
        ('netflix', 'Netflix'),
        ('amazon', 'Amazon Prime Video'),
        ('apple', 'Apple TV+'),
        ('manual', 'Ajout manuel'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='series',
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=200)
    tmdb_id = models.IntegerField(null=True, blank=True)
    overview = models.TextField(blank=True, default='')
    vote_average = models.FloatField(default=0.0)
    poster_path = models.CharField(max_length=500, blank=True, default='')
    provider = models.CharField(
        max_length=20, choices=PROVIDER_CHOICES, default='manual'
    )
    watched = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Série'
        verbose_name_plural = 'Séries'
        ordering = ['-created']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'tmdb_id'],
                condition=Q(tmdb_id__isnull=False),
                name='unique_user_tmdb',
            ),
        ]

    def __str__(self):
        return self.title

    def poster_url(self):
        if self.poster_path:
            return f'https://image.tmdb.org/t/p/w200{self.poster_path}'
        return ''
