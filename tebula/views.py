from django.shortcuts import render
from django.http import HttpResponse
from .modules.recipe import Recipe
from .modules.senders import get_sender_for
from .modules.crawler import crawl

sender = get_sender_for(platform='LINE')
current_recipe = None
current_recipe_changed=False


def register(request):
	global current_recipe
	global current_recipe_changed

	recipe_id = request.GET.get('recipe_id')
	try:
		current_recipe = crawl(recipe_id)
	except Exception as e:
		return HttpResponse(str(e))

	current_recipe_changed = True
	result = f'レシピID: {recipe_id} レシピタイトル: {current_recipe.content["title"]} が設定されました\n'

	try:
		sender.send_recipe(current_recipe)
		sender.send_step(current_recipe)
	except Exception as e:
		result += f'LINEとの通信に失敗しました: {str(e)}'
	
	return HttpResponse(result)

def recipe(request):
	if current_recipe:
		response = HttpResponse(f"レシピID: {current_recipe.recipe_id} が設定されています")
	else:
		response = HttpResponse("レシピIDが設定されていません")

	return response

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
	sender.send_step(current_recipe)

	response = HttpResponse(f"ステップ {current_recipe.step} になりました")
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