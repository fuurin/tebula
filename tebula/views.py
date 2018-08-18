import traceback
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from .modules.recipe import Recipe
from .modules.senders import get_sender_for
from .modules.crawler import crawl

sender = get_sender_for(platform='Dummy')
current_recipe = None
current_recipe_changed=False


def register(request):
	global current_recipe
	global current_recipe_changed

	recipe_id = request.GET.get('recipe_id')
	try:
		recipe_id = request.GET.get('recipe_id')
		current_recipe = crawl(recipe_id)
	except Exception as e:
		return HttpResponseBadRequest(str(e))

	current_recipe_changed = True
	result = f'レシピID: {recipe_id} レシピタイトル: {current_recipe.content["title"]} が設定されました\n'

	try:
		sender.send_recipe(current_recipe)
		sender.send_step(current_recipe)
	except Exception as e:
		result += f'{sender.platform}との通信に失敗しました: {str(e)}\n'
		result += traceback.format_exc()
	
	return HttpResponse(result)

def recipe(request):	
	if current_recipe:
		return JsonResponse({
			'recipe': {
				'recipe_id': current_recipe.recipe_id,
				'current_step': current_recipe.step,
				'content': current_recipe.content
			},
			'cooking': True
		})
	else:
		return JsonResponse({
			'recipe': {
				'recipe_id': None,
				'current_step': -1,
				'content': None
			},
			'cooking': False
		})


def current_step(request):
	if current_recipe:
		return JsonResponse({
			'current_step': current_recipe.step,
			'cooking': True
		})
	else:
		return JsonResponse({
			'current_step': -1,
			'cooking': False
		})

def step(request):
	if current_recipe:
		response = HttpResponse(f"今はステップ {current_recipe.step} です")
	else:
		response = HttpResponse("レシピIDが設定されていません")

	return response

def next_step(request):
	global current_recipe

	if not current_recipe:
		return HttpResponse("レシピIDが設定されていません")

	current_recipe.next_step()
	result = f"ステップ {current_recipe.step} になりました"
	try:
		sender.send_step(current_recipe)
	except Exception as e:
		result += f'{sender.platform}との通信に失敗しました: {str(e)}\n'
		result += traceback.format_exc()

	response = HttpResponse(result)
	if current_recipe.end:
		current_recipe = None
	return response

def listen(request):
    global current_recipe_changed
	if current_recipe_changed:
		current_recipe_changed = False
		return HttpResponse(current_recipe.content['title'])
	else:
		return HttpResponse("")

def change_sender(request):
	global sender
	try:
		platform = request.GET.get('platform')
		sender = get_sender_for(platform)
	except Exception as e:
		return HttpResponseBadRequest(str(e))
	if current_recipe:
		sender.send_recipe(current_recipe)
		sender.send_step(current_recipe)
	return HttpResponse(f'プラットフォームを{platform}に変更しました')
