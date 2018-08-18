import os
import json
import requests
from .templates.recipe import build as build_recipe
from .templates.step import build as build_step
from tebula.modules.senders.sender import BaseSender

class LINESender(BaseSender):

	ENV_CHHANNEL_ACCESS_TOKEN = 'LINE_CHANNEL_ACCESS_TOKEN'
	ENV_DESTINATION_ID = 'LINE_DESTINATION_ID'

	def __init__(self, channel_access_token=None, destination=None):
		self.platform='LINE'
		if channel_access_token is None:
			self.channel_access_token = os.getenv(
				LINESender.ENV_CHHANNEL_ACCESS_TOKEN
			)
		else:
			self.channel_access_token = channel_access_token

		if destination is None:
			self.destination = os.getenv(
				LINESender.ENV_DESTINATION_ID
			)
		else:
			self.destination = destination

		if self.channel_access_token is None:
			raise ValueError(
				f'cannot init LINESender: Missing channel access token.'
				f' Specify channel access token by argument or environment variable'
				f' {LINESender.ENV_CHHANNEL_ACCESS_TOKEN}.'
			)

		if self.destination is None:
			raise ValueError(
				f'cannot init LINESender: Missing sender destination.'
				f' Specify sender destination by argument or enviroment variable'
				f' {LINESender.ENV_DESTINATION_ID}'
			)

	def send_step(self, recipe):
		index = recipe.step
		n_steps = len(recipe.content['steps'])
		step = recipe.content['steps'][index]
		return self.send_flex(
			build_step({
				'index': index,
				'step': step['text'],
				'img_url': step['img_url'],
				'end': n_steps == index + 1,
			}),
			f'{index}. {step["text"]}'
		)

	def send_recipe(self, recipe):
		return self.send_flex(build_recipe(recipe.content), f'レシピ - {recipe.content.get("title", "(unknown)")}')

	def send_flex(self, contents, alt_text):
		headers = {
			'Authorization': f'Bearer {self.channel_access_token}'
		}
		responce = requests.post(
			url='https://api.line.me/v2/bot/message/push',
			headers=headers,
			json={
				"to": self.destination,
				"messages": [{
					"type": "flex",
					"altText": alt_text,
					"contents": contents
				}]
			}
		)
		responce.raise_for_status()


if __name__ == '__main__':
	sender = LINESender()
	with open('./crawl_result.json') as f:
		recipe = json.load(f)
	responce = sender.send_recipe(recipe)
	import time;
	sender.send_step(13, recipe)
