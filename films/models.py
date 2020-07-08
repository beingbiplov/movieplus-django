from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.urls import reverse

class FavFilm(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	film1 = models.CharField(max_length=25, blank=True)
	film2 = models.CharField(max_length=25, blank=True)
	film3 = models.CharField(max_length=25, blank=True)

	def __str__(self):
		return f'{self.user.username} FavFilm'

@receiver(post_save, sender=User)
def update_user_favfilm(sender, instance, created, **kwargs):
    if created:
        FavFilm.objects.create(user=instance)
    instance.profile.save()

class WatchedFilm(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	film = models.CharField(max_length = 25, blank=True)
	date_watched =  models.DateTimeField(default=timezone.now, blank=True)


	def __str__(self):
		return f'{self.user.username} WatchedFilm-{self.film}'

	


	

@receiver(post_save, sender=User)
def update_user_watchedfilm(sender, instance, created, **kwargs):
    if created:
        WatchedFilm.objects.create(user=instance)
    instance.profile.save()

class LikedFilm(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	film = models.CharField(max_length = 25, blank=True)
	date_watched =  models.DateTimeField(default=timezone.now, blank=True)


	def __str__(self):
		return f'{self.user.username} Liked-{self.film}'

@receiver(post_save, sender=User)
def update_user_likedfilm(sender, instance, created, **kwargs):
    if created:
        LikedFilm.objects.create(user=instance)
    instance.profile.save()

class Watchlist(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	film = models.CharField(max_length = 25, blank=True)
	date_watched =  models.DateTimeField(default=timezone.now, blank=True)

	def __str__(self):
		return f'{self.user.username} Watchlist-{self.film}'

@receiver(post_save, sender=User)
def update_user_watchlist(sender, instance, created, **kwargs):
    if created:
        Watchlist.objects.create(user=instance)
    instance.profile.save()


# class Review(models.Model):
# 	user = models.ForeignKey(User, on_delete=models.CASCADE)
# 	film = models.CharField(max_length = 25, blank=True)
# 	review = models.TextField()
# 	rating = models.IntegerField(null=True)
# 	date_reviewed =  models.DateTimeField(default=timezone.now, blank=True)

# 	def __str__(self):
# 		return f'{ self.user.username }-{ self.film }'

# @receiver(post_save, sender=User)
# def update_user_review(sender, instance, created, **kwargs):
#     if created:
#         Review.objects.create(user=instance)
#     instance.profile.save()