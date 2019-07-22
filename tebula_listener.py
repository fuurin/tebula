import os
import json
from time import sleep
from datetime import datetime
import requests
import subprocess
import pychromecast


# CURRENT_RECIPE_URL = "http://127.0.0.1:8000/current_recipe/"
# CURRENT_STEP_URL = "http://127.0.0.1:8000/current_step/"
CURRENT_RECIPE_URL = "https://tebula.herokuapp.com/current_recipe/"
CURRENT_STEP_URL = "https://tebula.herokuapp.com/current_step/"
RESET_URL = "https://tebula.herokuapp.com/reset/"

SOUND_NAME = 'sound.mp3'

# LOCAL_SERVER_BASE_URL = "http://127.0.0.1:3000/"

INTERVAL = 2

casts = pychromecast.get_chromecasts()
cast = casts[0]
print(cast)

recipe = None
step = -1
while True:
    sleep(INTERVAL)
    r_recipe = requests.get(CURRENT_RECIPE_URL)
    r_step = requests.get(CURRENT_STEP_URL)

    current_recipe_json = json.loads(r_recipe.text)
    current_step_json = json.loads(r_step.text)

    print(datetime.now())
    print(current_recipe_json)
    print(current_step_json)

    text = ""

    if current_recipe_json['recipe']['current_step'] != -1:
        current_recipe_id = int(current_recipe_json['recipe']['recipe_id'])
        if recipe is None or current_recipe_id != int(recipe['recipe']['recipe_id']):
            recipe = current_recipe_json
            recipe_title = recipe['recipe']['content']['title']
            step = -1
            text = recipe_title+"のレシピが登録されました。"

    if recipe is not None:
        current_step = int(current_step_json['current_step'])
        if current_step != -1 and current_step != step:
            step = current_step
            text += f"手順{step+1}、{recipe['recipe']['content']['steps'][step]['text']}"
            if step+1 == len(recipe['recipe']['content']['steps']):
                text = text.rstrip("。") + "。完成です。"
                r_reset = requests.get(RESET_URL)
            print(text)
            res = subprocess.run(["node", "play.js", text])
            text = ""