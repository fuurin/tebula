def build(params):
	ingredients = [
		{
			"type": "box",
			"layout": "horizontal",
			"contents": [
				{
					"type": "text",
					"text": f"{ing.get('name', '(unknown)')}",
					"size": "sm",
					"color": "#555555",
					"flex": 0
				},
				{
					"type": "text",
					"text": f"{ing.get('quantity', '(unknown)')}",
					"size": "sm",
					"color": "#111111",
					"align": "end"
				}
			]
		}
		for ing in params['ingredients']
	]
	ingredients_header = {
		"type": "text",
		"text": f"材料 ({params.get('servings', '(unknown)人分')})",
		"weight": "bold",
		"color": "#1DB446",
		"size": "sm",
		"margin": "xxl",
	}
	action = {
		"type": "uri",
		"uri": params.get('source_url', '(unknown)'),
	},
	return {
		"type": "bubble",
		"header": {
			"type": "box",
			"layout": "vertical",
			"contents": [
				{
					"type": "text",
					"text": "進行中のレシピ",
					"weight": "bold",
					"color": "#1DB446",
					"size": "sm"
				},
				{
					"type": "text",
					"text": params.get('title', '(unknown)'),
					"weight": "bold",
					"size": "xl",
					"margin": "md",
					"wrap": True,
				},
			]
		},
		"hero": {
			"type": "image",
			"url": params.get('img_url', '(unknown)'),
			"size": "full",
			"aspectRatio": "20:13",
			"aspectMode": "cover",
		},
		"body": {
			"type": "box",
			"layout": "vertical",
			"margin": "xxl",
			"spacing": "sm",
			"contents": [ingredients_header] + ingredients
		},
		"footer": {
			"type": "box",
			"layout": "horizontal",
			"contents": [
				{
					"type": "text",
					"text": "進むには、「次のステップ」と話しかけてください。",
					"weight": "bold",
					"color": "#aaaaaa",
					"size": "sm",
					"wrap": True,
				}
			]
		}
	}
