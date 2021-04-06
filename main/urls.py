from . import views
from django.urls import path


urlpatterns = [
    path('', views.seasons, name='seasons'),
    path('episodes/<int:episode_id>', views.episode_detail, name='episode_detail'),
    path('<str:series>/<int:season>', views.episodes, name='episodes'),
    path('characters/<str:name>', views.character_detail, name='character'),
    path('search', views.character_list, name='search'),
]