# coding=utf-8
import openpyxl
import os
import selenium
import stat
import bs4
import time
import requests
import re
import sys
import subprocess

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

#Globals
i = 0
URL = ''
text = ()
replaced = ()
replacedtext = ()

def URLBuilder():
    global i
    global URL
    while i > 0 :
        URL = ('https://careers.kaspersky.ru/bitrix/admin/iblock_element_edit.php?IBLOCK_ID=28&type=portal&ID=' + str(i) + '&lang=ru&find_section_section=0&WF=Y')
        print(URL)
        return URL

def Replacer():
    global text
    global replaced
    #global replacedtext
    #Находим ключевые места по регуляркам
    #первый абзац
    replaced = re.sub('это 4 000 экспертов', 'это 4&nbsp;000 экспертов', text)
    replaced = re.sub('возможность стать настоящим героем, оставаясь самим собой.', 'возможность стать настоящим героем, оставаясь самим собой.<p></p>', replaced)
    replaced = re.sub('24 часа в сутки спасаем мир от киберугроз.<br>', '24 часа в сутки спасаем мир от киберугроз.<p></p><br>', replaced)
    replaced = re.sub('"«Лаборатория Касперского»', '<p>«Лаборатория Касперского»', replaced)
    replaced = re.sub('"Не хватает технических', '<p>Не хватает технических', replaced)
    #заголовки
    replaced = re.sub('Мы предлагаем:', '</ul><h3>Мы предлагаем:</h3><br><ul>', replaced)
    replaced = re.sub('Обязанности:', '<br></ul><h3>Обязанности:</h3><br><ul>', replaced)
    replaced = re.sub('Что надо будет делать?', '<br></ul><h3>Что надо будет делать?</h3><br><ul>', replaced)
    replaced = re.sub('Что надо будет делать:', '<br></ul><h3>Что надо будет делать:</h3><br><ul>', replaced)
    replaced = re.sub('Мы рассчитываем, что вы умеете:', '<br></ul><h3>Мы рассчитываем, что вы умеете:<br></h3><br><ul>', replaced)
    replaced = re.sub('Мы ждем, что у вас есть:', '<br></ul><h3>Мы ждем, что у вас есть:</h3><br><ul>', replaced)
    replaced = re.sub('Плюсом будет, если у вас есть:', '<br></ul><h3>Плюсом будет, если у вас есть:</h3><br><ul>', replaced)
    #replaced = re.sub('Не предлагаем:<br>', '</ul><h3>Не предлагаем:</h3><ul>', replaced)
    replaced = re.sub('Не предлагаем:', '</ul><h3>Не предлагаем:</h3><ul>', replaced)
    replaced = re.sub('Необходимый опыт:', '</p><br></ul><h3>Необходимый опыт:</h3><ul>', replaced)
    replaced = re.sub('Чего мы ждем:', '</p><br></ul><h3>Чего мы ждем:</h3><ul>', replaced)
    replaced = re.sub('Желательно, но не обязательно:', '</ul><h3>Желательно, но не обязательно:</h3><br><ul>', replaced)
    replaced = re.sub('Плюсом будет:', '</ul><h3>Плюсом будет:</h3><ul>', replaced)
    replaced = re.sub('Будет плюсом:', '</ul><h3>Будет плюсом:</h3><ul>', replaced)
    replaced = re.sub('Мы ожидаем:', '</ul><h3>Мы ожидаем:</h3><br><ul>', replaced)
    replaced = re.sub('Ключевые задачи:', '<h3>Ключевые задачи:</h3><ul>', replaced)
    replaced = re.sub('Требования:', '<br></ul><h3>Требования:</h3><ul>', replaced)
    replaced = re.sub('Нужно уметь:', '</ul><h3>Нужно уметь</h3><ul>', replaced)
    replaced = re.sub('Не обязательно, но будет плюсом:', '</ul><h3>Не обязательно, но будет плюсом:</h3><br><ul>', replaced)
    replaced = re.sub('Желательно:', '</ul><h3>Желательно:</h3><br><ul>', replaced)
    #основной текст
    replaced = re.sub('"21 год на рынке', '<p>21 год на рынке', replaced)
    replaced = re.sub('"О нас в цифрах:', '<p>О нас в цифрах:', replaced)
    replaced = re.sub('• ', '	<li>', replaced)
    #replaced = re.sub('<br>\n', '</li>', replaced)
    replaced = re.sub('мес"', 'мес', replaced)
    replaced = re.sub('--', '—', replaced)
    #завершающие фразы
    replaced = re.sub('Программа релокации для будущих сотрудников и их семей"', 'Программа релокации для будущих сотрудников и их семей<br><br>', replaced)
    replaced = re.sub('Унылых коллег"', 'Унылых коллег', replaced)
    replaced = re.sub('унылых коллег"', 'Унылых коллег', replaced)
    replaced = re.sub('вы наверняка слышали!"', 'вы наверняка слышали!', replaced)
    replaced = re.sub('вы, наверняка, слышали!"', 'вы, наверняка, слышали!', replaced)
    # тут такая проблема, похоже что если тег ul не открыть и начать фигачить li -- то всё это дело вылетает из админки, рандомно нажимая все клавиши внизу страницы
    replacedtext = replaced
    print(replacedtext)

def ReplacedTextPutin():
    global text
    global driver
    time.sleep(5)
    sendctrla = driver.find_element_by_xpath('//*[@id="bxed_DETAIL_TEXT"]').send_keys(Keys.CONTROL, "a")
    time.sleep(1)
    senddelete = driver.find_element_by_xpath('//*[@id="bxed_DETAIL_TEXT"]').send_keys(Keys.DELETE)
    time.sleep(0.3)
    #pastetext = driver.find_element_by_css_selector('#bxed_DETAIL_TEXT').send_keys(replacedtext)
    time.sleep(1)
    pastetextnew = driver.execute_script(document.find_element_by_css_selector('#bxed_DETAIL_TEXT')[0].click())
    #driver.find_element_by_css_selector('#save').click()
    time.sleep(2)

def GetVacancy():
    global text
    global driver
    #driver = webdriver.Chrome('C:\ChromeDriver\chromedriver.exe')  # Optional argument, if not specified will search path.
    driver.get(URL)
    if i == min:
        print(input('say some if you\'re ready:'))
    podrobnotap = driver.find_element_by_css_selector('#tab_cont_edit2')
    podrobnotap.click()
    time.sleep(2)
    HTMLbutton = driver.find_element_by_css_selector('#bxed_DETAIL_TEXT_html')
    HTMLbutton.click()
    time.sleep(2)
    textonsite = driver.find_element_by_css_selector("#bxed_DETAIL_TEXT").text
    text = ('\'\'\'' + textonsite + '\'\'\'')
    Replacer()
    ReplacedTextPutin()


for repeater in range (0, 100, 1):
    min = int(input('Welcome to vacancy typofraph v 0.000001a. Please enter the vacancy_id_min:'))
    max = int(input('Great! Min = ' + str(min) + '!, for now enter the vacancy_id_max:'))
    print('I\'m starting the browser')
    driver = webdriver.Chrome('C:\ChromeDriver\chromedriver.exe')
    for i in range (min, max, 1):
        URLBuilder()
        GetVacancy()
    debreaker = input('Repeat? (y/n):')
    if debreaker == 'y': continue
    if debreaker == 'n': break
