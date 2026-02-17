from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('', views.index, name="list"),
    path('series/<str:pk>/', views.detail_series, name="detail"),
    path('series/<str:pk>/toggle/', views.toggle_watched, name="toggle_watched"),
    path('series/<str:pk>/delete/', views.delete_series, name="delete"),
    path(
        'import/<str:provider>/',
        views.import_series,
        name="import_series",
    ),
]
