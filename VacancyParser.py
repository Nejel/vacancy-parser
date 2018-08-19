# -*- coding: utf-8 -*-

import docx
import re
import os
import csv


cwd = os.getcwd() + '\\'
filename = 'results.csv'
content = [] # глобальная переменная для контента перед записью в csv


def Search(fullText): # функция поиска по тексту. Вызывается функцией получения текста
    #print('Search', fullText)
    findURL = re.findall('https://\S+|http://\S+', str(fullText), flags = 0)
    #print('SearchURL', findURL)
    findRecruit = re.findall('Таня|Валя|Никита|Даша Мелкова|[А-Я][а-я]\S+ [А-Я][а-я]\S+\bЛаборатория \b', str(fullText), flags = 0)
    #print('Searchrecruit', findRecruit)
    finddescription = re.findall('У нас \S+|Тут \S+|Описание .+', str(fullText), flags = 0)
    searchresults = findURL, findRecruit, finddescription
    #print('searchresults', searchresults)
    return searchresults

def getText(filename): # функция получения текста из файла.
                        # Вызывается главной функцией ReadFolderAndFiles
    doc = docx.Document(filename)
    fullText = []
    i = 0
    while i < 1:
        for para in doc.paragraphs:
            #print(type(fullText)) # list
            fullText.append(para.text)
        URLsearchResults = Search(fullText) # tuple # вызываем поиск по тексту
        fullText = URLsearchResults
        i += 1
    return fullText # list

def ReadFolderAndFiles(content):
    #foldername = (input('Enter a folder name: ')) # ждем ввода папки
    foldername = ('vacancies') # по умолчанию установлена папка vacancies
    cwd2 = cwd + foldername # собираем конструктор пути файла
    for x in (os.listdir(cwd2)):
        filename = cwd2 + '\\' + x # собираем конструктор пути файла
        #print(filename)
        #print(getText(filename))
        content.append(getText(filename)) # list # добавляем в конец листа
        #fullcontent = ''.join(content)
    return content # происходит выход из функции после завершения цикла for, в глобальное пространтсов возвращается значение контент


ReadFolderAndFiles(content) # вызываем функцию с параметром, чтобы вернуть значение

with open(filename, 'a', encoding='utf8', newline = '') as file: #готовим файл к записи в utf-8
    writer = csv.writer(file, delimiter=',', quotechar='"')
    #print(dir(writer))
    writer.writerows(content) # пишем в файл из глобальной переменной контент
