import os
from time import sleep
import requests
import pychromecast
from gtts import gTTS
import boto3
import boto3.s3.transfer

URL = "http://127.0.0.1:8000/listen"
# URL = "https://tebula.herokuapp.com/listen"

SOUND_NAME = 'sound.mp3'

AWS_SOUND_BASE_URL = "https://s3-ap-northeast-1.amazonaws.com/tebula/"

INTERVAL = 2

BUCKET_NAME = "tebula"

config = boto3.s3.transfer.TransferConfig(use_threads=False)

s3 = boto3.resource('s3')
bucket = s3.Bucket(BUCKET_NAME)

while True:
    sleep(INTERVAL)
    r = requests.get(URL)
    if r.text:
        print(r.text)
        casts = pychromecast.get_chromecasts()
        cast = casts[0]
        
        tts = gTTS(text=r.text+'のレシピが登録されました', lang='ja')
        tts.save(SOUND_NAME)
        bucket.upload_file(SOUND_NAME, SOUND_NAME, Config=config)
        cast.media_controller.play_media(AWS_SOUND_BASE_URL + SOUND_NAME, 'audio/mp3')

        # s3.Object(BUCKET_NAME, SOUND_NAME).delete()
        # os.remove(SOUND_NAME)