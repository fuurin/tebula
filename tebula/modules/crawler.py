import requests
import json
from bs4 import BeautifulSoup
import emoji
from .recipe import Recipe


def crawl(recipe_id):
    recipe = dict()
    source_url = "https://cookpad.com/recipe/{}".format(recipe_id)
    r = requests.get(source_url)
    if r.status_code != 200:
        raise ValueError(f'Recipe (recipe_id={recipe_id}) not found.')

    html = r.text
    soup = BeautifulSoup(html)

    def get_title():
        title = soup.h1.text.strip()
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
        return servings


    def get_ingredient(ingredient_tag):
        name = ingredient_tag.find("div", class_="ingredient_name").text.strip()
        quantity = ingredient_tag.find("div", class_="ingredient_quantity").text.strip()
        return {"name": name, "quantity": quantity}


    def get_ingredients():
        ingredients = []
        for ingredient_tag in soup.find_all("div", class_="ingredient_row"):
            try:
                ingredients.append(get_ingredient(ingredient_tag))
            except:
                pass
        return ingredients


    def get_step(step_tag):
        step = step_tag.text.strip()
        step_id = step_tag['id'].split('_')[-1]
        div_tag = soup.find("div", id="recipe-step_photo_{}".format(step_id))
        img_tag = div_tag.find("img")
        if img_tag:
            img_url = img_tag["src"]
        else:
            img_url = ""
        return {"text": step, "img_url": img_url}

    
    def get_steps():
        steps = []
        for step_tag in soup.find_all("p", class_="step_text"):
            step = get_step(step_tag)
            if step:
                steps.append(step)
        return steps

    recipe['success'] = True
    recipe['source_url'] = source_url
    recipe['title'] = get_title()
    recipe['img_url'] = get_img_url()
    recipe['servings'] = get_servings()
    recipe['ingredients'] = get_ingredients()
    recipe['steps'] = get_steps()

    return Recipe(
        recipe_id=recipe_id,
        content=recipe
    )
