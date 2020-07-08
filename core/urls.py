from django.urls import path
from . import views
from .views import UserProfile, UserInfoCreateView


app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    path('details/<int:movie_id>', views.details, name='details'),
    path('user/<username>',views.profile, name='profiles'),
    path('user/info/', UserInfoCreateView.as_view(), name='user-info'),
    path('userinfo/<int:pk>/update', UserProfile.as_view(), name='info-update'),

]
