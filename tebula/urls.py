from django.urls import path
from django.urls.conf import include
from .views import register, recipe, step, next_step, change_sender, current_step, reset

urlpatterns = [
	path('register/', register, name='register'),
	path('step/', step, name='step'),
	path('next_step/', next_step, name='next_step'),
	path('change_sender/', change_sender, name='change_sender'),
	path('current_step/', current_step, name='current_step'),
	path('current_recipe/', recipe, name='recipe'),
	path('reset/', reset, name='reset')
]