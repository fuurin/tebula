import os
import json
from time import sleep
import requests
import subprocess
import pychromecast
from gtts import gTTS
import boto3
import boto3.s3.transfer


CURRENT_RECIPE_URL = "http://127.0.0.1:8000/current_recipe/"
CURRENT_STEP_URL = "http://127.0.0.1:8000/current_step/"
# CURRENT_RECIPE_URL = "https://tebula.herokuapp.com/current_recipe/"
# CURRENT_STEP_URL = "https://tebula.herokuapp.com/current_step/"

SOUND_NAME = 'sound.mp3'

# LOCAL_SERVER_BASE_URL = "http://127.0.0.1:3000/"

AWS_SOUND_BASE_URL = "https://s3-ap-northeast-1.amazonaws.com/tebula/"

INTERVAL = 2

BUCKET_NAME = "tebula"

config = boto3.s3.transfer.TransferConfig(use_threads=False)

s3 = boto3.resource('s3')
bucket = s3.Bucket(BUCKET_NAME)

casts = pychromecast.get_chromecasts()
cast = casts[0]

recipe = None
step = -1

while True:
    sleep(INTERVAL)
    r = requests.get(CURRENT_RECIPE_URL)
    current_recipe = json.loads(r.text)
    if current_recipe['cooking']:
        current_recipe_id = int(current_recipe['recipe']['recipe_id'])
        if recipe is None or current_recipe_id != int(recipe['recipe']['recipe_id']):
            recipe = current_recipe
            recipe_title = recipe['recipe']['content']['title']
            step = -1
            res = subprocess.run(["node", "play.js", recipe_title+"のレシピが登録されました"])
            sleep(8)

    r = requests.get(CURRENT_STEP_URL)
    res_json = json.loads(r.text)
    if res_json['cooking']:
        current_step = int(res_json['current_step'])
        if current_step != step:
            step = current_step
            res = subprocess.run(["node", "play.js", recipe['recipe']['content']['steps'][step]['text']])