from .senders import LINESender
import json

class Recipe():
	def __init__(self, recipe_id, content):
		self.__recipe_id = recipe_id
		self.__recipe_step = 0
		self.__content = content

	@property
	def recipe_id(self):
		return self.__recipe_id

	@property
	def step(self):
		return self.__recipe_step

	def next_step(self):
		self.__recipe_step += 1

	def prev_step(self):
		self.__recipe_step -= 1

	@property
	def end(self):
		return self.__recipe_step >= len(self.__content['steps']) - 1

	@property
	def content(self):
		return self.__content
