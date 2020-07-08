from django.contrib import admin
from .models import FavFilm, WatchedFilm, LikedFilm

admin.site.register(FavFilm)
admin.site.register(WatchedFilm)
admin.site.register(LikedFilm)