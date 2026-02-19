from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="list"),
    path('series/<str:pk>/', views.detail_series, name="detail"),
    path('series/<str:pk>/toggle/', views.toggle_watched, name="toggle_watched"),
    path('series/<str:pk>/delete/', views.delete_series, name="delete"),
    path(
        'import/<str:provider>/',
        views.import_series,
        name="import_series",
    ),
    # Authentification
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('france-connect/', views.france_connect_authorize, name='france_connect_authorize'),
    path('callback', views.france_connect_callback, name='france_connect_callback'),
]
