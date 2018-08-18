import os
import requests
from slackclient import SlackClient
from .templates.step import build as build_step
from .templates.recipe import build as build_recipe

class SlackSender:

	ENV_WORKSPACE_ACCESS_TOKEN = 'SLACK_WORKSPACE_ACCESS_TOKEN'
	ENV_DESTINATION_ID = 'SLACK_DESTINATION_ID'

	def __init__(self, workspace_access_token=None, destination=None):
		self.platform = 'Slack'
		if workspace_access_token is None:
			self.workspace_access_token = os.getenv(
				SlackSender.ENV_WORKSPACE_ACCESS_TOKEN
			)
		else:
			self.workspace_access_token = workspace_access_token

		self.client = SlackClient(self.workspace_access_token)

		if destination is None:
			self.destination = os.getenv(
				SlackSender.ENV_DESTINATION_ID
			)
		else:
			self.destination = destination

		if self.workspace_access_token is None:
			raise ValueError(
				f'cannot init SlackSender: Missing workspace access token.'
				f' Specify workspace access token by argument or environment variable'
				f' {LINESender.ENV_WORKSPACE_ACCESS_TOKEN}.'
			)

		if self.destination is None:
			raise ValueError(
				f'cannot init SlackSender: Missing sender destination.'
				f' Specify sender destination by argument or enviroment variable'
				f' {LINESender.ENV_DESTINATION_ID}'
			)

	def send_recipe(self, recipe):
		self.send_attachments(build_recipe(recipe))

	def send_step(self, recipe):
		self.send_attachments(attachments=build_step(recipe))

	def send_attachments(self, attachments=None):
		responce = self.client.api_call(
			"chat.postMessage",
			channel=self.destination,
			attachments=attachments,
			as_user=True,
			text='',
		)

