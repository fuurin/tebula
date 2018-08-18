def build(params):
	ret = {
		"type": "bubble",
		"header": {
			"type": "box",
			"layout": "vertical",
			"contents": [
				{
					"type": "box",
					"layout": "horizontal",
					"spacing": "xl",
					"contents": [
						{
							"type": "text",
							"text": f"{params.get('index', 0) + 1}",
							"size": "xl",
							"color": "#555555",
							"align": "center",
							"gravity": "center",
							"weight": "bold",
							"flex": 0
						},
						{
							"type": "text",
							"text": f"{params.get('step', '(unknown)')}",
							"size": "sm",
							"color": "#111111",
							"wrap": True
						}
					]
				}
			]
		},
	}
	img_url = params.get("img_url", None)
	if img_url:
		ret["hero"] = {
			"type": "image",
			"url": img_url,
			"size": "full",
			"aspectRatio": "20:13",
			"aspectMode": "cover",
		}
	if params.get("end"):
		ret["body"] = {
			"type": "box",
			"layout": "vertical",
			"spacing": "xl",
			"contents": [
				{
					"type": "text",
					"text": u"\U0001F389",
					"size": "xxl",
					"color": "#555555",
					"align": "center",
					"gravity": "center",
					"flex": 0
				},
				{
					"type": "text",
					"text": f"完成です！",
					"size": "md",
					"color": "#111111",
					"align": "center",
					"weight": "bold",
					"wrap": True
				}
			]
		}
	return ret
