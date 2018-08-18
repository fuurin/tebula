from django.shortcuts import render
from django.http import HttpResponse
from .modules.user_data import userdata

def register(request):

	recipe_id = request.GET.get('recipe_id')

	userdata.recipe_id = recipe_id

	if userdata.isset() and userdata.scraping_result['success']:
    		response = HttpResponse("レシピID: {0} レシピタイトル: {1} が設定されました".format(userdata.recipe_id, userdata.scraping_result['title']))
	else:
		response = HttpResponse("そのレシピIDは存在しません")
	
	return response

def recipe(request):

	if userdata.isset():
		response = HttpResponse("レシピID: {0} が設定されています".format(userdata.recipe_id))
	else:
		response = HttpResponse("レシピIDが設定されていません")

	return response

def step(request):

	if userdata.isset():
		response = HttpResponse("今はステップ {0} {1} です".format(userdata.recipe_step, userdata.scraping_result["steps"][userdata.recipe_step]["text"]))
	else:
		response = HttpResponse("レシピIDが設定されていません")

	return response

def next_step(request):
	
	if userdata.isset():
		userdata.next_step()
		try:
			response = HttpResponse("ステップ {0} {1} になりました".format(userdata.recipe_step, userdata.scraping_result["steps"][userdata.recipe_step]["text"]))
		except IndexError:
			response = HttpResponse("これ以上ステップはありません")
	else:
		response = HttpResponse("レシピIDが設定されていません")

	return response