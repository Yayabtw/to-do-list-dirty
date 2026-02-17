from django.db import models


class Series(models.Model):
    """Model representing a TV series in the watchlist."""

    PROVIDER_CHOICES = [
        ('netflix', 'Netflix'),
        ('amazon', 'Amazon Prime Video'),
        ('apple', 'Apple TV+'),
        ('manual', 'Ajout manuel'),
    ]

    title = models.CharField(max_length=200)
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)
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

    def __str__(self):
        return self.title

    def poster_url(self):
        if self.poster_path:
            return f'https://image.tmdb.org/t/p/w200{self.poster_path}'
        return ''
