def build(recipe):
    ingredients = [
        {
            'title': ing['name'],
            'value': f'{ing["quantity"]}',
            'short': True,
        }
        for ing in recipe.content['ingredients']
    ]
    attachments = [
        {
            "fallback": "Recipe step.",
            "color": "#E93226",
            "title": recipe.content['title'],
            "title_link": recipe.content['source_url'],
            "image_url": recipe.content['img_url'],
            "fields": ingredients,
        }
    ]
    return attachments
