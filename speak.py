import requests
import pygame
from time import sleep
import config

from enum import Enum

class Emotion(Enum):
    GOOD='good'
    NEUTRAL='neutral'
    EVIL='evil'

class Speaker(Enum):
    JANE='jane'
    OKSANA='oksana'
    ALYSS='alyss'
    OMAZH='omazh'
    ZAHAR='zahar'
    ERMIL='ermil'


def speak(text, emotion=Emotion.EVIL, speed=1.2, speaker=Speaker.JANE):
    response = requests.get('https://tts.voicetech.yandex.net/generate', params={
        'key': config.YA_KEY,
        'text': text,
        'lang': 'ru-RU',
        'quality': 'hi', #'lo', # 'hi'
        'speaker': speaker.value,
        'speed': speed,
        'emotion': emotion.value,
    })
    pygame.mixer.init()
    channel = pygame.mixer.Sound(buffer=response.content).play()
    return channel

def speak_sync(text):
    channel = speak(text)
    while channel.get_busy():
        sleep(0.3)
