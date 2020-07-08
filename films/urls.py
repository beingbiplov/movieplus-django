from django.urls import path
from . import views

urlpatterns = [
    path('fav', views.Fav, name='fav'),
    path('addfav/<movie_id>', views.AddFav, name='addfav'),
    path('removefav/<movie_id>', views.RemoveFav, name='removefav'),
    path('watched/<movie_id>', views.AddWatched, name='addwatched'),
    path('removewatched/<movie_id>', views.removeWatched, name='removewatched'),
    path('addliked/<movie_id>', views.addLiked, name='addliked'),
    path('removeliked/<movie_id>', views.removeLiked, name='removeliked'),
    path('addwatchlist/<movie_id>', views.addWatchlist, name='addwatchlist'),
    path('removewatchlist/<movie_id>', views.removeWatchlist, name='removewatchlist'),
    path('addreview/<movie_id>', views.addReview, name='addReview'),

]
