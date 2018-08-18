from django.urls import path
from django.urls.conf import include
from .views import register, next_step

urlpatterns = [
	path('register/', register, name='register'),
	path('next_step/', next_step, name='next_step'),
]