from django.shortcuts import render
from django.http import HttpResponse
from .modules.user_data import userdata

def register(request):

	recipe_id = request.GET.get('recipe_id')

	userdata.recipe_id = recipe_id

	if userdata.isset():
		response = HttpResponse("レシピID: {0} レシピタイトル: {1} が設定されました".format(userdata.recipe_id, userdata.scraping_result['title']))
	else:
		response = HttpResponse("不正なレシピID")
	
	return response

def recipe(request):

	if userdata.isset():
		response = HttpResponse("レシピID: {0} が設定されています".format(userdata.recipe_id))
	else:
		response = HttpResponse("レシピIDが設定されていません")

	return response

def step(request):

	if userdata.isset():
		response = HttpResponse("今はステップ {0} です".format(userdata.recipe_step))
	else:
		response = HttpResponse("レシピIDが設定されていません")

	return response

def next_step(request):
	
	if userdata.isset():
		userdata.next_step()
		response = HttpResponse("ステップ {0} になりました".format(userdata.recipe_step))
	else:
		response = HttpResponse("レシピIDが設定されていません")

	return response