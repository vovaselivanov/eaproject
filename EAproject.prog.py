# импорт необходимых модулей
 
import pyttsx3
import os
import random
import webbrowser
import time
import speech_recognition as sr
import pandas as pd
from tkinter import *
from fuzzywuzzy import fuzz
from colorama import *
 
# раздел глобальных переменных
 
text = ''
r = sr.Recognizer()
engine = pyttsx3.init()
adress = ''
j = 0
task_number = 0
 
ndel = ['екатерина александровна', 'катя', 'екатерина', 'катенька']
 
commands = ['привет', 'пока', 'открой youtube', 'переведи', 'планы', "ctime", "radio", "stupid1",
"search", "createide", "about", "online_course", "online_vebinar", "contacts", "news", "gallery"]
 
# раздел описания функций комманд
 
def pri_com(): # выводит на экран историю запросов
    z = {}
    mas = []
    mas2 = []
    mas3 = []
    mas4 = []
    file = open('commands.txt', 'r', encoding = 'UTF-8')
    k = file.readlines()
    for i in range(len(k)):
        line = str(k[i].replace('\n','').strip())
        mas.append(line)
    file.close()
    for i in range(len(mas)):
        x = mas[i]
        if x in z:
            z[x] += 1
        if not(x in z):
            b = {x : 1}
            z.update(b)
        if not(x in mas2):
            mas2.append(x)
    for i in mas2:
        mas3.append(z[i])
    for i in range(1, len(mas3)+1):
        mas4.append(str(i)+') ')    
    list = pd.DataFrame({
        'command' : mas2,
        'count' : mas3
    }, index = mas4)
    list.index.name = '№'
    print(list)
 
def clear_analis(): # очистка файла с историей запросов
    global engine
    file = open('commands.txt', 'w', encoding = 'UTF-8')
    file.close()
    engine.say('Файл аналитики очищен!')
 
def add_file(x):
    file = open('commands.txt', 'a',encoding = 'UTF-8')
    if x != '':
        file.write(x+'\n')
    file.close()    
 
def comparison(x): # осуществляет поиск самой подходящей под запрос функции
    global commands,j,add_file
    ans = ''
    for i in range(len(commands)):
        k = fuzz.ratio(x,commands[i])
        if (k > 50)&(k > j):
            ans = commands[i]
            j = k
    if (ans != 'пока')& (ans != 'привет'):
        add_file(ans)
    return(str(ans))
 
def web_search(): # осуществляет поиск в интернете по запросу (adress)
    global adress
    webbrowser.open('https://yandex.ru/yandsearch?clid=2028026&text={}&lr=11373'.format(adress))
 
def check_searching(): # проверяет нужно-ли искать в интернете
    global text,wifi_name,add_file
    global adress
    global web_search
    if 'найди' in text:
        add_file('найди')
        adress = text.replace('найди','').strip()
        text = text.replace(adress,'').strip()
        web_search()
        text = ''
    elif 'найти' in text:
        add_file('найди')
        adress = text.replace('найти','').strip()
        text = text.replace(adress,'').strip()
        web_search()
        text = ''
    adress = ''
 

def hello(): # функция приветствия
    global engine
    z = ["Рада снова вас слышать!", 'Что вам угодно?', 'Привет. Чем-нибудь помочь?']
    x = random.choice(z)
    engine.say(x)
 
def quit(): # функция выхода из программы
    global engine
    x = ['надеюсь мы скоро увидемся!', 'рада была помочь', 'всегда к вашим услугам']
    engine.say(random.choice(x))
    engine.runAndWait()
    engine.stop()
    os.system('cls')
    exit(0)


def youtube(): # открывает ютюб
    webbrowser.open('https://www.youtube.com')

def createide():
    webbrowser.open('https://rsv.ru/account/proposal/create')

def about():
    webbrowser.open('https://rsv.ru/portal/about-us')

def online_course():
    webbrowser.open('https://rsv.ru/portal/edu/courses/1/334')

def online_vebinar():
    webbrowser.open('https://rsv.ru/portal/edu/webinars/1/141')

def contacts():
    webbrowser.open('https://rsv.ru/portal/contacts')

def news():
    webbrowser.open('https://rsv.ru/portal/news/1/1623')

def gallery():
    webbrowser.open('https://rsv.ru/portal/gallery')

def check_translate():
    global text, tr
    tr = 0
    variants = ['переведи', 'перевести', 'переводить', 'перевод']
    for i in variants:  
        if (i in text)&(tr == 0):
            word = text
            word = word.replace('переведи','').strip()
            word = word.replace('перевести','').strip()
            word = word.replace('переводить','').strip()
            word = word.replace('перевод','').strip()
            word = word.replace('слово','').strip()
            word = word.replace('слова','').strip()
            webbrowser.open('https://translate.google.ru/#view=home&op=translate&sl=auto&tl=ru&text={}'.format(word))
            tr = 1
            text = ''
 
cmds = {
    'привет':hello,
    'пока':quit,
    'открой youtube':youtube,
    'у меня есть инициатива':createide,
    'переведи':check_translate,
    'что такое россия страна возможностей':about,
    'хочу на онлайн курсы':online_course,
    'хочу на вебинар':online_vebinar,
    'как связаться':contacts,
    'новости':news,
    'фотографии':gallery
}
 
# распознавание
 
def talk(): 
    global text, clear_task
    text = ''
    with sr.Microphone() as sourse:
        print('Я вас слушаю: ')
        r.adjust_for_ambient_noise(sourse)
        audio = r.listen(sourse, phrase_time_limit=3)
        try:
            text = (r.recognize_google(audio, language="ru-RU")).lower()    
        except(sr.UnknownValueError):
            pass
        except(TypeError):
            pass
        os.system('cls')
        lb['text'] = text
        clear_task()
 
# выполнение команд
 
def cmd_exe():
    global cmds, engine, comparison, check_searching, task_number, text, lb
    check_translate()
    text = comparison(text)
    print(text)
    check_searching()
    if (text in cmds):
        if (text != 'привет') & (text != 'пока') & (text != 'покажи список команд'):
            k = ['Секундочку', 'Сейчас сделаю', 'уже выполняю']
            engine.say(random.choice(k))
        cmds[text]()
    elif text == '':
        pass
    else:
        print('Команда не найдена!')
    task_number += 1
    if (task_number % 10 == 0):
        engine.say('У вас будут еще задания?')
    engine.runAndWait()
    engine.stop()
 
print(Fore.YELLOW + '', end = '')
os.system('cls')
 
# бесконечный цикл
 
def main():
    global text, talk, cmd_exe, j
    try:
        talk()
        if text != '':
            cmd_exe()
            j = 0
    except(UnboundLocalError):
        pass
    except(TypeError):
        pass
 
# раздел создания интерфейса
 
root = Tk()
root.geometry('350x450')
root.configure(bg = 'white')
root.title('EAproject')
root.resizable(False, False)
 
lb = Label(root, text = text)
lb.configure(bg = 'gray')
lb.place(x = 25, y = 25, height = 25, width = 300)
 
but1 = Button(root, text = 'Говорить', command = main)
but1.configure(bd = 1, font = ('Castellar', 25), bg = 'gray')
but1.place(x = 90, y = 160, height = 50, width = 150)
 
but2 = Button(root, text = 'Выход', command = quit)
but2.configure(bd = 1, font = ('Castellar',25), bg = 'gray')
but2.place(x = 90, y = 220, height = 50, width = 150)
 
root.mainloop()
 
while True:
    main()