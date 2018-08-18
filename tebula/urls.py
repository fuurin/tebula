from django.urls import path
from django.urls.conf import include
from .views import register, recipe, step, next_step, change_sender

urlpatterns = [
	path('register/', register, name='register'),
	path('recipe/', recipe, name='recipe'),
	path('step/', step, name='step'),
	path('next_step/', next_step, name='next_step'),
	path('change_sender/', change_sender, name='change_sender')
]