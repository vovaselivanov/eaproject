import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import webbrowser

opts = {
    "alias": ('екатерина александровна', 'катя', 'екатерина', 'катенька'),
    "tbr": ('скажи','расскажи','покажи','сколько','произнеси'),
    "cmds": {
        "ctime": ('текущее время','сейчас времени','который час','сколько времени'),
        "radio": ('включи музыку','воспроизведи радио','включи радио'),
        "stupid1": ('расскажи анекдот','рассмеши меня','ты знаешь анекдоты'),
        "search" : ('что такое', "найди"),
        "createide": ('как подать свою инициативу','хочу свой конкурс','у меня есть инициатива'),
        "about": ('что такое россия страна возможностей','россия страна возможностей','россия страна возможностей это','рсв'),
        "online-course": ('хочу на онлайн курс','хочу на онлайн курсы','какие есть онлайн курсы','записаться на онлайн курс','записаться на онлайн курсы','хочу на курсы','записаться на курсы'),
        "online-vebinar": ('хочу на онлайн вебинар','хочу на вебинар','какие есть онлайн вебинары','записаться на вебинар','записаться на онлайн вебинар'),
        "contacts": ('контакты','адрес','подписка','указ президента','связаться с нами'),
        "news": ('новости','известия','актуальное','вести','связаться с нами'),
        "gallery": ('галерея','фото','фотографии','изображения','фотография')
    }
}


# функции
def speak(what):
    print( what )
    speak_engine.say( what )
    speak_engine.runAndWait()
    speak_engine.stop()

def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
        print("[log] Распознано: " + voice)
        if voice.startswith(opts["alias"]):
            # обращаются к Кеше
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()
            
            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()
            
            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")

def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c,v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    
    return RC

def execute_cmd(cmd):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
    
    elif cmd == 'radio':
        # воспроизвести радио
        webbrowser.open_new_tab('https://online-red.com/radio/Umor-FM.html')
    
    elif cmd == 'stupid1':
        # рассказать анекдот
        speak("Я бы мог научиться юмору, но в данной компании не у кого учиться, ааххха")
    
    elif cmd == 'search':
        webbrowser.open_new_tab('https://yandex.ru/search/?text='.format(cmd)),
        speak("Открываю поиск. Пип пип пип")

    elif cmd == 'createide':
        webbrowser.open_new_tab('https://rsv.ru/account/proposal/create'.format(cmd)),
        speak("Открываю страницу...")

    elif cmd == 'about':
        webbrowser.open_new_tab('https://rsv.ru/portal/about-us'.format(cmd)),
        speak("Открываю страницу...")

    elif cmd == 'online-course':
        webbrowser.open_new_tab('https://rsv.ru/portal/edu/courses/1/334'.format(cmd)),
        speak("Открываю страницу...")

    elif cmd == 'online-vebinar':
        webbrowser.open_new_tab('https://rsv.ru/portal/edu/webinars/1/141'.format(cmd)),
        speak("Открываю страницу...")

    elif cmd == 'contacts':
        webbrowser.open_new_tab('https://rsv.ru/portal/contacts'.format(cmd)),
        speak("Открываю страницу...")

    elif cmd == 'news':
        webbrowser.open_new_tab('https://rsv.ru/portal/news/1/1623'.format(cmd)),
        speak("Открываю страницу...")

    elif cmd == 'gallery':
        webbrowser.open_new_tab('https://rsv.ru/portal/gallery'.format(cmd)),
        speak("Открываю страницу...")

    else:
        print('Команда не распознана, повторите!')
# запуск
r = sr.Recognizer()
m = sr.Microphone(device_index = 1)

with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()

# Только если у вас установлены голоса для синтеза речи!
#voices = speak_engine.getProperty('voices')
#speak_engine.setProperty('voice', voices[6].id)

#forced cmd test
#speak("Мой разработчик не научил меня анекдотам ... Ха ха ха")

speak("Здраствуй!")
speak("Я тебя внимательно слушаю...")

stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1) # infinity loop