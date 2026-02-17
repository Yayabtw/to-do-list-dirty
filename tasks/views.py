import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from .models import Series

TMDB_BASE_URL = 'https://api.themoviedb.org/3'

PROVIDER_IDS = {
    'netflix': 8,
    'amazon': 119,
    'apple': 350,
}

PROVIDER_LABELS = {
    'netflix': 'Netflix',
    'amazon': 'Amazon Prime Video',
    'apple': 'Apple TV+',
}


def _fetch_series_from_tmdb(provider_key, user, count=10):
    """Fetch top-rated series from TMDB for a given provider.

    Returns up to `count` series that are NOT already in the user's watchlist,
    by paginating through TMDB results as needed.
    """
    provider_id = PROVIDER_IDS[provider_key]
    existing_tmdb_ids = set(
        Series.objects.filter(user=user, tmdb_id__isnull=False)
        .values_list('tmdb_id', flat=True)
    )

    headers = {
        'Authorization': f'Bearer {settings.TMDB_API_TOKEN}',
        'accept': 'application/json',
    }

    new_series = []
    page = 1
    max_pages = 10

    while len(new_series) < count and page <= max_pages:
        params = {
            'sort_by': 'vote_average.desc',
            'with_watch_providers': provider_id,
            'watch_region': 'FR',
            'with_watch_monetization_types': 'flatrate',
            'vote_count.gte': 100,
            'language': 'fr-FR',
            'page': page,
        }

        response = requests.get(
            f'{TMDB_BASE_URL}/discover/tv',
            headers=headers,
            params=params,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        results = data.get('results', [])

        if not results:
            break

        for show in results:
            tmdb_id = show['id']
            if tmdb_id not in existing_tmdb_ids:
                new_series.append({
                    'title': show.get('name', 'Sans titre'),
                    'tmdb_id': tmdb_id,
                    'overview': show.get('overview', ''),
                    'vote_average': show.get('vote_average', 0),
                    'poster_path': show.get('poster_path', ''),
                    'provider': provider_key,
                })
                existing_tmdb_ids.add(tmdb_id)

            if len(new_series) >= count:
                break

        page += 1

    return new_series


@login_required
def index(request):
    """View for listing all series in the watchlist."""
    series_list = Series.objects.filter(user=request.user)

    context = {
        'series_list': series_list,
        'version': settings.VERSION,
    }
    return render(request, 'tasks/list.html', context)


@login_required
def detail_series(request, pk):
    """View for displaying series details."""
    series = get_object_or_404(Series, id=pk, user=request.user)
    context = {'series': series}
    return render(request, 'tasks/detail.html', context)


@login_required
def toggle_watched(request, pk):
    """Toggle the watched status of a series."""
    if request.method == 'POST':
        series = get_object_or_404(Series, id=pk, user=request.user)
        series.watched = not series.watched
        series.save()
    return redirect('detail', pk=pk)


@login_required
def delete_series(request, pk):
    """View for deleting a series from the watchlist."""
    item = get_object_or_404(Series, id=pk, user=request.user)

    if request.method == "POST":
        item.delete()
        return redirect('/')

    context = {'item': item}
    return render(request, 'tasks/delete.html', context)


def login_view(request):
    """Custom login view so the form receives request and username is stripped."""
    if request.user.is_authenticated:
        return redirect('list')
    if request.method == 'POST':
        # Strip username to avoid "wrong credentials" due to spaces
        post = request.POST.copy()
        if 'username' in post:
            post['username'] = post['username'].strip()
        form = AuthenticationForm(request, data=post)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.POST.get('next') or request.GET.get('next') or settings.LOGIN_REDIRECT_URL
            return redirect(next_url)
    else:
        form = AuthenticationForm(request)
    return render(request, 'tasks/login.html', {'form': form, 'next': request.GET.get('next', '')})


def register(request):
    """View for user registration."""
    if request.user.is_authenticated:
        return redirect('list')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Compte créé. Bienvenue !')
            return redirect('list')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/register.html', {'form': form})


@login_required
def import_series(request, provider):
    """Import 10 series from a streaming provider via TMDB API."""
    if request.method != 'POST':
        return redirect('/')

    if provider not in PROVIDER_IDS:
        messages.error(request, f'Fournisseur inconnu : {provider}')
        return redirect('/')

    try:
        new_series = _fetch_series_from_tmdb(provider, request.user, count=10)

        created_count = 0
        for s in new_series:
            Series.objects.create(user=request.user, **s)
            created_count += 1

        label = PROVIDER_LABELS[provider]
        if created_count > 0:
            messages.success(
                request,
                f'{created_count} séries {label} ajoutées à la watchlist !'
            )
        else:
            messages.info(
                request,
                f'Aucune nouvelle série {label} à ajouter '
                f'(toutes déjà présentes).'
            )

    except requests.RequestException as e:
        messages.error(
            request,
            f'Erreur lors de la récupération des séries : {e}'
        )

    return redirect('/')
