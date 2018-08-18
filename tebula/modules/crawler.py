import requests
import json
from bs4 import BeautifulSoup
import emoji


def remove_emoji(s):
    return "".join(c for c in s if c not in emoji.UNICODE_EMOJI)


def crawl(recipe_id, do_remove_emoji=True):

    recipe = dict()
    source_url = "https://cookpad.com/recipe/{}".format(recipe_id)
    r = requests.get(source_url)
    if r.status_code != 200:
        recipe['success'] = 0
        return json.dumps(recipe)

    html = r.text
    soup = BeautifulSoup(html)


    def get_title():
        title = soup.h1.text.strip()
        if do_remove_emoji:
            title = remove_emoji(title)
        return title

    def get_img_url():
        try:
            img_url = soup.find("img", class_="analytics_tracking photo large_photo_clickable")["data-large-photo"]
            return img_url
        except TypeError:
            return ""


    def get_servings():
        try:
            servings = soup.find("span", class_="servings_for").text.strip().strip("(（）)")
        except AttributeError:
            return ""
        
        if do_remove_emoji:
            servings = remove_emoji(servings)
        return servings


    def get_ingredient(ingredient_tag):
        name = ingredient_tag.find("div", class_="ingredient_name").text.strip()
        quantity = ingredient_tag.find("div", class_="ingredient_quantity").text.strip()
        if do_remove_emoji:
            name = remove_emoji(name)
            quantity = remove_emoji(quantity)
        return {"name": name, "quantity": quantity}


    def get_ingredients():
        ingredients = []
        for ingredient_tag in soup.find_all("div", class_="ingredient_row"):
            ingredients.append(get_ingredient(ingredient_tag))
        return ingredients


    def get_step(step_tag):
        step = step_tag.text.strip()
        if do_remove_emoji:
            step = remove_emoji(step)
        return step

    
    def get_steps():
        steps = []
        for step_tag in soup.find_all("p", class_="step_text"):
            step = get_step(step_tag)
            if step:
                steps.append(step)
        return steps

    recipe['success'] = 1
    recipe['source_url'] = source_url
    recipe['title'] = get_title()
    recipe['img_url'] = get_img_url()
    recipe['servings'] = get_servings()
    recipe['ingredients'] = get_ingredients()
    recipe['steps'] = get_steps()

    return json.dumps(recipe)