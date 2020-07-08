from django.shortcuts import render
import requests
from django.conf import settings
from .models import UserInfo
from user.models import Profile
from films.models import FavFilm, WatchedFilm, LikedFilm, Watchlist
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def index(request):

	movies =[]
	popular_movies =[]
	upcoming_movies=[]

	api_key =settings.MOVIE_API_KEY
	

	url = 'https://api.themoviedb.org/3/search/movie?api_key={0}&query={1}'
	image_url='https://image.tmdb.org/t/p/w500/{}'
	query_url = 'https://api.themoviedb.org/3/movie/343611?api_key={}'
	popular_url ='https://api.themoviedb.org/3/movie/popular?api_key={}&language=en-US&page=1'
	upcomming_url = "https://api.themoviedb.org/3/movie/upcoming?api_key={}"


	if request.method == 'POST':
		query = request.POST['search']
		query = query.replace(" ",'+')
		url = url.format(api_key, query)
	
		r= requests.get(url)
		result = r.json()
		

		results = result['results']
		
		
		for movie in results:
			movie_data= {
				'title': movie['original_title'],
				'overview': movie['overview'],
				'poster_path' : image_url.format(movie['poster_path']),
				'id' :movie['id'],
				'release_date' : movie['release_date'],
				'language' : movie['original_language'].upper(),

			}

			movies.append(movie_data)
		context = {'movies': movies}


		return render(request, 'core/index.html' , context)

	popular_parse_url = popular_url.format(api_key)

	w = requests.get(popular_parse_url)
	popular_result = w.json()

	pop_results = popular_result['results']
		
		
	for movie in pop_results:
		movie_data= {
			'title': movie['original_title'],
			'overview': movie['overview'],
			'poster_path' : image_url.format(movie['poster_path']),
			'id' :movie['id'],
			'release_date' : movie['release_date'],
			'language' : movie['original_language'].upper(),

		}
		popular_movies.append(movie_data)
	

	#Upcomming movies
	upcomming_parse_url = upcomming_url.format(api_key)
	u = requests.get(upcomming_parse_url)
	upcomming_result= u.json()

	upcomming_results = upcomming_result['results']

	for movie in upcomming_results:
		movie_data= {
			'title': movie['original_title'],
			'overview': movie['overview'],
			'poster_path' : image_url.format(movie['poster_path']),
			'id' :movie['id'],
			'release_date' : movie['release_date'],
			'language' : movie['original_language'].upper(),

		}
		upcoming_movies.append(movie_data)

	
	context = {
		'popular_movies' : popular_movies,
		'upcoming_movies' : upcoming_movies,
	}

	

	
	


	return render(request, 'core/index.html', context)


def details(request ,movie_id):

	

	if request.user.is_authenticated:
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
		
	else:
		fav= False
		watched_this=False
		liked = False
		watchlisted = False
	
	

	api_key =settings.MOVIE_API_KEY
	movie=[]
	cast_details=[]
	crew_details =[]
	genres =[]
	movie_details=[]
	directors =[]
	producers = []

	image_url='https://image.tmdb.org/t/p/w500/{}'
	query_url = 'https://api.themoviedb.org/3/movie/{}?api_key={}&append_to_response=credits'
	imdb_url = 'https://www.imdb.com/title/{}'
	video_url ='https://api.themoviedb.org/3/movie/{}?api_key={}&append_to_response=videos'
	trailer_url ='https://www.youtube.com/watch?v={}'
	rating_url = 'https://api.themoviedb.org/3/movie/{}?api_key={}&append_to_response=releases'
	
	url = query_url.format(movie_id, api_key)
	r= requests.get(url)
	result = r.json()

	
	


	video_parse_url = video_url.format(movie_id, api_key)
	v = requests.get(video_parse_url)
	video_result = v.json()

	video_details = {
		'trailer_url' : trailer_url.format(video_result['videos']['results'][0]['key'])
	}

	


	

	movie_data ={
		'title' : result['original_title'],
		'overview': result['overview'],
		'tagline' : result['tagline'],
		'poster_path' : image_url.format(result['poster_path']),
		'id' :result['id'],
		'release_date' : result['release_date'],
		'language' : result['original_language'].upper(),
		'budget' : result['budget'],
		'genre' : result['genres'][0]['name'],
		'runtime' : result['runtime'],
		'revenue' : result['revenue'],
		'imdb_url': imdb_url.format(result['imdb_id']),
		'movie_url' :result['homepage'],
		'backdrop_path' : image_url.format(result['backdrop_path']),

	}
	movie.append(movie_data)

	movie_detail= {
		'title' : result['original_title'],
		'release_date' : result['release_date'],
		'language' : result['original_language'].upper(),
		'budget' : result['budget'],
		'genre' : result['genres'][0]['name'],
		'runtime' : result['runtime'],
		'revenue' : result['revenue'],


	}
	movie_details.append(movie_detail)

	for job in result['credits']['crew']:
		if job['job'] == 'Director':
			director = {
				'name' : job['name']
			}
			directors.append(director)

	
	for job in result['credits']['crew']:
		if job['job'] == 'Producer':
			producer = {
				'name' : job['name']
			}
			producers.append(producer)

	

	for genre in result['genres']:
		gen = {
			'genre' : genre['name']
		}
		genres.append(gen)

	



	for cast in result['credits']['cast']:
		cast_detail ={
			'name' : cast['name'],
			'character' : cast['character'],
		}
		cast_details.append(cast_detail)
	
	for crew in result ['credits']['crew']:
		crew_detail= {
			'name' : crew['name'],
			'department' : crew['department'],
			'job' : crew['job'],
			'crew_url' :crew['profile_path'],
		}
		crew_details.append(crew_detail)

	

	context = {
		'movie':movie,
		'genres' : genres,
		'cast_details': cast_details,
		'crew_details' : crew_details,
		'directors' : directors,
		'producers': producers,
		'movie_details' : movie_details,
		'video_details' : video_details,
		'fav': fav,
		'watched_this' : watched_this,
		'liked' : liked,
		'watchlisted' : watchlisted,
	}

	
	return render(request, 'core/details.html', context)


def profile(request, username):
	fav_films=[]
	watched_films =[]
	liked_films = []
	watchlist_films = []

	api_key =settings.MOVIE_API_KEY
	
	short_query_url = 'https://api.themoviedb.org/3/movie/{}?api_key={}'
	query_url = 'https://api.themoviedb.org/3/movie/{}?api_key={}&append_to_response=credits'
	image_url='https://image.tmdb.org/t/p/w500/{}'

	loggedin_user = request.user.username
	profile_user = username

	if loggedin_user == profile_user:
		edit = True
	else:
		edit = False


	userdata = Profile.objects.get(user__username=profile_user)
	
	userinfo = UserInfo.objects.get(user__username=profile_user)

	favfilms = FavFilm.objects.get(user__username=profile_user)

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

		for movie_id in movie_ids:
			url = query_url.format(movie_id, api_key)
			r= requests.get(url)
			result = r.json()
			

			movie_data ={
			'title' : result['title'],
			'poster_path' : image_url.format(result['poster_path']),
			'id' :result['id'],
			}
			fav_films.append(movie_data)
		

#watched movies ....ython
	watched_list = WatchedFilm.objects.all().filter(user__username=profile_user).order_by('-date_watched')
	watched_movies=[]
	for films in watched_list:
		watched_movies.append(films.film)
	
	
	for movie_id in watched_movies:
		
		url = short_query_url.format(movie_id, api_key)
		r= requests.get(url)
		result = r.json()
		
		try:
			movie_data ={
				'title' : result['title'],
				'poster_path' : image_url.format(result['poster_path']),
				'id' :result['id'],
				}
			watched_films.append(movie_data)
		except:
			pass
	
	liked_list = LikedFilm.objects.all().filter(user__username=profile_user).order_by('-date_watched')
	liked_movies=[]
	for movies in liked_list:
		liked_movies.append(movies.film)

	for movie_id in liked_movies:
		
		url = short_query_url.format(movie_id, api_key)
		r= requests.get(url)
		result = r.json()
		
		try:
			movie_data ={
				'title' : result['title'],
				'poster_path' : image_url.format(result['poster_path']),
				'id' :result['id'],
				}
			liked_films.append(movie_data)
		except:
			pass

	watchlist = Watchlist.objects.all().filter(user__username=profile_user).order_by('-date_watched')
	wl_movies = []
	for movies in watchlist:
		wl_movies.append(movies.film)

	for movie_id in wl_movies :
		
		url = short_query_url.format(movie_id, api_key)
		r= requests.get(url)
		result = r.json()
		
		try:
			movie_data ={
				'title' : result['title'],
				'poster_path' : image_url.format(result['poster_path']),
				'id' :result['id'],
				}
			watchlist_films.append(movie_data)
		except:
			pass
	#Review list
	# reviewList = Review.objects.all().filter(user__username=profile_user).order_by('-date_reviewed')
	# reviewed_movies =[]
	# for movies in reviewList:
	# 	url = short_query_url.format(movies.film, api_key)
	# 	r= requests.get(url)
	# 	result = r.json()
	# 	print(result)
	# 	movie_data={
	# 		'title' : result['title'],
	# 		'review' : movies.review,
	# 		'rating' : movies.rating,
	# 		'review_date' : movies.date_reviewed
	# 	}
	# 	reviewed_movies.append(movie_data)

	context = {
		'userdata' : userdata,
		'edit' : edit,
		'userinfo' : userinfo,
		'fav_films' : fav_films,
		'watched_films': watched_films,
		'liked_films' : liked_films,
		'watchlist_films' : watchlist_films,
		#'reviewed_movies' : reviewed_movies


	}

	return render(request, 'core/profile.html', context)

	

class UserInfoCreateView(LoginRequiredMixin , CreateView):
	model = UserInfo
	fields = [ 'bio', 'location', 'website', 'twitter_handle']
	template_name = 'core/add_user_info.html'

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

class UserProfile(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = UserInfo
	fields=['bio', 'location', 'website', 'twitter_handle']
	template_name = 'core/update_user_info.html'

	def test_func(self):
		Userinfo = self.get_object()

		if self.request.user == Userinfo.user:
			return True
		return False
