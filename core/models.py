from django.db import models
from django.contrib.auth.models import User
from user.models import Profile
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserInfo(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	bio = models.CharField(max_length = 140, blank=True)
	location = models.CharField(max_length=45, blank=True)
	website = models.URLField(max_length=250, blank=True)
	twitter_handle = models.CharField(max_length=15, blank=True)

	def __str__(self):
		return f'{self.user.username} Info'

	def get_absolute_url(self):
		return reverse('core:profiles', kwargs={'username': self.user})

#to automatically populate UserInfo model with default data when user is created
@receiver(post_save, sender=User)
def update_user_userinfo(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(user=instance)
    instance.profile.save()


