from django.shortcuts import render
from django.http import HttpResponse

def register(request):
	recipe_id = request.GET.get('recipe_id')

	if recipe_id and recipe_id.isdigit():
		response = HttpResponse("レシピID{0}".format(recipe_id))
	else:
		response = HttpResponse("不正なレシピID")
	
	return response

def next_step(request):
	return HttpResponse("次のステップ")