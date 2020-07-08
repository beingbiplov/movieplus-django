from django.shortcuts import render, redirect
import requests
from django.conf import settings
from .models import FavFilm, WatchedFilm, LikedFilm, Watchlist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect

@login_required
def Fav(request):
	movies =[]
	fav_films = []
	total_fav =0

	api_key =settings.MOVIE_API_KEY
	

	url = 'https://api.themoviedb.org/3/search/movie?api_key={0}&query={1}'
	image_url='https://image.tmdb.org/t/p/w500/{}'
	query_url = 'https://api.themoviedb.org/3/movie/{}?api_key={}&append_to_response=credits'

	user = request.user.username
	favfilms = FavFilm.objects.get(user__username=user)

	if favfilms.film1 != "":
		total_fav += 1
	if favfilms.film2 != "":
		total_fav += 1
	if favfilms.film3 != "":
		total_fav += 1
	

	if request.method == 'POST':
		query = request.POST['search']
		query = query.replace(" ",'+')
		url = url.format(api_key, query)
	
		r= requests.get(url)
		result = r.json()
		

		results = result['results']
		
		
		for movie in results:
			movie_data= {
				'title': movie['title'],
				'poster_path' : image_url.format(movie['poster_path']),
				'id' :movie['id'],
				'release_date' : movie['release_date'],
				'language' : movie['original_language'].upper(),

			}

			movies.append(movie_data)
		context = {'movies': movies, 
				'total_fav' : total_fav,
		}



		return render(request, 'films/addfav.html' , context)


	if favfilms.film1 == "" and favfilms.film2 == "" and favfilms.film3 == "":
		fav_films = []

	else:
		movie_ids = []
		if favfilms.film1 != "":
			movie_ids.append(favfilms.film1)
		if favfilms.film2 != "":
			movie_ids.append(favfilms.film2)

		if favfilms.film3 != "":
			movie_ids.append(favfilms.film3)
		# print(movie_ids)

		for movie_id in movie_ids:
			url = query_url.format(movie_id, api_key)
			r= requests.get(url)
			result = r.json()
			# print(result)
			

			movie_data ={
			'title' : result['title'],
			'poster_path' : image_url.format(result['poster_path']),
			'id' :result['id'],
			'release_date' : result['release_date'],
			'language' : result['original_language'].upper(),
			}
			fav_films.append(movie_data)
		


	context ={
		'total_fav' : total_fav,
		'fav_films' : fav_films,
	}

	return render(request,'films/addfav.html',  context)

@login_required
def AddFav(request, movie_id):
	user = request.user.username
	favfilms = FavFilm.objects.get(user__username=user)

	
	
	if favfilms.film1 != movie_id and favfilms.film2 != movie_id and favfilms.film3 != movie_id:

		if favfilms.film1 == "":
			FavFilm_instance = FavFilm.objects.filter(user=request.user).update(user=request.user, film1=movie_id)
			
		elif favfilms.film2 == "":
			FavFilm_instance = FavFilm.objects.filter(user=request.user).update(user=request.user, film2=movie_id)
			
		elif favfilms.film3 == "":
			FavFilm_instance = FavFilm.objects.filter(user=request.user).update(user=request.user, film3=movie_id)
			
		else:
			messages.info(request, f'Your fav film list is full')
			return redirect('fav')
	else:
		messages.info(request, f'The film you are trying to add is already in your fav list')
		return redirect('fav')


	

	messages.success(request, f'Added to your fav films.')
	return redirect('fav')

@login_required
def RemoveFav(request, movie_id):
	user = request.user.username
	favfilms = FavFilm.objects.get(user__username=user)
	# print(favfilms)

	if favfilms.film1 != movie_id and favfilms.film2 != movie_id and favfilms.film3 != movie_id:
		messages.warning(request, f'The film you are trying to remove is not in your fav list!!')
		return redirect('fav')

		
	else:
		if favfilms.film1 == movie_id:
			FavFilm_instance = FavFilm.objects.filter(user=request.user).update(user=request.user, film1="")
			
		elif favfilms.film2 == movie_id:
			FavFilm_instance = FavFilm.objects.filter(user=request.user).update(user=request.user, film2="")
			
		elif favfilms.film3 == movie_id:
			FavFilm_instance = FavFilm.objects.filter(user=request.user).update(user=request.user, film3="")

	messages.success(request, f'Successfully removed from your Favorite.')
	return redirect('fav')

@login_required
def AddWatched(request, movie_id):
	user = request.user.username

	watched_list = WatchedFilm.objects.all().filter(user__username=request.user.username)
	watched_movies=[]
	for films in watched_list:
		watched_movies.append(films.film)

	if str(movie_id) in watched_movies:
		messages.warning(request, f'The movie is already in watched list')

	else:	
		WatchedFilm_instance = WatchedFilm.objects.create(user=request.user, film=movie_id)
		messages.success(request, f'Successfully added to your watched list.')
		
	return redirect('core:details', movie_id=movie_id)
	


@login_required
def removeWatched(request, movie_id):
	watched_list = WatchedFilm.objects.all().filter(user__username=request.user.username)
	watched_movies=[]
	for films in watched_list:
		watched_movies.append(films.film)

	if str(movie_id) in watched_movies:
		WatchedFilm.objects.filter(film = movie_id).delete()
		messages.success(request, f'The movie is removed from your watched list')
	else:
		messages.warning(request, f'The movie is not in your watched list')

	return redirect('core:details', movie_id=movie_id)


@login_required
def addLiked(request, movie_id):
	liked_list = LikedFilm.objects.all().filter(user__username=request.user.username)
	liked_movies=[]
	for films in liked_list:
		liked_movies.append(films.film)

	if str(movie_id) in liked_movies:
		messages.warning(request, f'The movie is already in liked list')
	else:
		WatchedFilm_instance = LikedFilm.objects.create(user=request.user, film=movie_id)
		messages.success(request, f'Successfully added to your Liked list.')

	return redirect('core:details', movie_id=movie_id)

@login_required
def removeLiked(request, movie_id):
	liked_list = LikedFilm.objects.all().filter(user__username=request.user.username)
	liked_movies=[]
	for films in liked_list:
		liked_movies.append(films.film)

	if str(movie_id) in liked_movies:
		LikedFilm.objects.filter(film = movie_id).delete()
		messages.success(request, f'The movie is removed from your liked list')
	else:
		messages.warning(request, f'You have not liked this movie')

	return redirect('core:details', movie_id=movie_id)

@login_required
def addWatchlist(request, movie_id):
	watched_list = Watchlist.objects.all().filter(user__username=request.user.username)
	wl_movies = []
	for films in watched_list:
		wl_movies.append(films.film)

	if str(movie_id) in wl_movies:
		messages.warning(request, f'This movie is already in your Watchlist')
	else:
		Watchlist_instance = Watchlist.objects.create(user=request.user, film=movie_id)
		messages.success(request, f'Successfully added to your Watchlist.')

	return redirect('core:details', movie_id=movie_id)

@login_required
def removeWatchlist(request, movie_id):
	watched_list = Watchlist.objects.all().filter(user__username=request.user.username)
	wl_movies = []
	for films in watched_list:
		wl_movies.append(films.film)

	if str(movie_id) in wl_movies:
		Watchlist.objects.filter(film = movie_id).delete()
		messages.success(request, f'The movie is removed from your Watchlist')
	else:
		messages.warning(request, f'This movie is not in your Watchlist')

	return redirect('core:details', movie_id=movie_id)

@login_required
def addReview(request, movie_id):

	api_key =settings.MOVIE_API_KEY
	
	query_url = 'https://api.themoviedb.org/3/movie/{}?api_key={}&append_to_response=credits'
	image_url='https://image.tmdb.org/t/p/w500/{}'
	imdb_url = 'https://www.imdb.com/title/{}'

	review_list = Review.objects.all().filter(user__username=request.user.username)
	review_movies = []
	for films in review_list:
		review_movies.append(films.film)

	if str(movie_id) in review_movies:
		messages.warning(request, f'You have already reviewed this movie. ')
	else:

		if request.method == 'POST':
			user_review = request.POST['review']
			user_rating = request.POST['optradio']

			# print(f'{ user_review } - { user_rating }')
			Review_instance = Review.objects.create(user=request.user, film=movie_id, review= user_review, rating = user_rating)
			messages.success(request, f'You have Successfully reviewed this movie. ')
			return redirect('core:details', movie_id=movie_id)

		else:
			movie_datas=[]
			url = query_url.format(movie_id, api_key)
			r= requests.get(url)
			result = r.json()
			# print(result)

			favfilms = FavFilm.objects.get(user__username=request.user.username)
			watched_list = WatchedFilm.objects.all().filter(user__username=request.user.username)
			watched_movies=[]
			for films in watched_list:
				watched_movies.append(films.film)
			
			fav_list = [favfilms.film1, favfilms.film2, favfilms.film3]

			liked_list = LikedFilm.objects.all().filter(user__username=request.user.username)
			liked_movies=[]
			for movies in liked_list:
				liked_movies.append(movies.film)

			watchlist = Watchlist.objects.all().filter(user__username=request.user.username)
			wl_movies = []
			for movies in watchlist:
				wl_movies.append(movies.film)
			
			if str(movie_id) in liked_movies:
				liked = True
			else:
				liked = False

			if str(movie_id) in fav_list:
				fav = True
			else:
				fav = False
			
			if str(movie_id) in wl_movies:
				watchlisted = True
			else:
				watchlisted = False

			if str(movie_id) in watched_movies:
				watched_this = True
			else:
				watched_this = False
			

			movie_data ={
			'title' : result['title'],
			'poster_path' : image_url.format(result['poster_path']),
			'id' :result['id'],
			'release_date' : result['release_date'],
			'backdrop_path' : image_url.format(result['backdrop_path']),
			'movie_url' :result['homepage'],
			'imdb_url': imdb_url.format(result['imdb_id']),
			'movie_url' :result['homepage']
			}
			movie_datas.append(movie_data)

			context ={
				'movie_data' : movie_datas,
				'fav': fav,
				'watched_this' : watched_this,
				'liked' : liked,
				'watchlisted' : watchlisted,
			}

			return render(request, 'films/review.html', context)
			#Watchlist_instance = Review.objects.create(user=request.user, film=movie_id)
			#messages.success(request, f'You have Successfully reviewed this movie.')

	return redirect('core:details', movie_id=movie_id)



