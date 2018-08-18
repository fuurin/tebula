def build(recipe):
    attachments = [
        {
            "fallback": "Recipe step.",
            "color": "#E93226",
            "title": recipe.step + 1,
            "text": recipe.content['steps'][recipe.step]['text'],
        }
    ]
    image_url = recipe.content['steps'][recipe.step]['img_url']
    if image_url:
        attachments[0]['image_url'] = image_url
    if recipe.end:
        attachments[0]["text"] += "\n\n:tada:  完成です!"
    return attachments
