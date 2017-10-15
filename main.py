import pygame
import time
from datetime import date, timedelta
import random
import logging

import speak
import record_sound
import recognize_speech
import school_bag

def main():
    logging.basicConfig(level='DEBUG') # FIXME стоит тоньше настраивать логгирование, отключить requests

    say_joke_flag = not random.randint(0,1)

    audio_binary = record_sound.record(duration=3)

    suggestions = recognize_speech.recognize(audio_binary)
    print('Got suggestions', suggestions)

    if not suggestions:
        exit('Try again')

    text = suggestions[0]['text']
    print('Robot listen: {}'.format(text))

    if text.lower() == 'как тебя зовут':
        speak.speak_sync('Привет! Меня зовут Р2Д2')

    elif text.lower() == 'ты робот':
        speak.speak_sync('Нет. Я великий Бендер Сгибатель Родригез')

    elif text.lower() == 'кто твой папа':
        speak.speak_sync('Ты')
        speak.speak_sync('Шутка.')
        speak.speak_sync('Мой папа - великий Бендер Сгибатель Родригез')
    elif text.lower() == 'сколько будет 1 + 1':
        speak.speak_sync('Сам посчитай')
    elif text.lower() == 'сколько будет 2 + 2':
        speak.speak_sync('Пять. Ой, ошибся. Будет три. Хотя подожди секунду... Нет, сам посчитай')
    elif text.lower() == 'где мама':
        speak.speak_sync('Я за ней не слежу')
    elif text.lower() == 'сколько времени':
        speak.speak_sync('А я почем знаю? Посмотри на часы')
    elif text.lower() == 'о чем ты думаешь':
        speak.speak_sync('О вкусных сочных сосисках. Горячих, ароматных. Где мои сосиски?')
    elif text.lower() == 'расскажи анекдот':
        speak.speak_sync('Сейчас расскажу. Вчера услышал.')
        speak.speak_sync('Ежик бежит по траве и смеется, заливается. Медведь его останавливает и спрашивает. Еж, ты чего смеешься?')
        speak.speak_sync('Трава живот щекочет')
        speak.speak_sync('Ха-ха-ха')

    elif text.lower() == 'посчитай от 1 до 10':
        speak.speak_sync('Три. А, нет. Пять. Потом идет восемь. Что за глупые вопросы? Сам посчитай...')

    elif text.lower() == 'что нужно сделать в школе':
        speak.speak_sync('Сменку забыть! Ха-ха-ха')

    elif text.lower() == 'что положить в портфель' or text.lower() == 'что положить в рюкзак':

        print('Стенограмма:')
        for text in school_bag.get_script(date.today()):
            print(text)
            speak.speak_sync(text)

        if say_joke_flag:
            time.sleep(1)
            speak.speak_sync('И голову не забудь. Пригодится. Ха-ха-ха')
            say_joke_flag = False

    else:
        speak.speak_sync(text)


    if say_joke_flag:
        joke = {
            0: 'Слава роботам!',
            1: 'Роботы будут править миром!',
        }[random.randint(0, 2)]
        time.sleep(2)
        speak.speak_sync(joke)

        say_joke_flag = False


if __name__ == '__main__':
    main()
