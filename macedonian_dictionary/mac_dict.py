#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import urllib.request
import urllib.error
import urllib.parse


#-----чтение страницы, возвращает ?текст страницы-----
def open_page(url):
    req = urllib.request.Request(url, data=None, headers={'User-Agent': 'Safari'})
    f = urllib.request.urlopen(req)
    a = f.read().decode() #('UTF-8')
    f.close()
    return a

#-----создание и запись в файл-----
def w_in_file(f_name, w_text):
    f = open(f_name, 'w', encoding='utf-8')
    f.write(w_text)
    f.close()

#-----чтение файла-----
def r_file(f_name):
    f = open(f_name, 'r', encoding='utf-8')
    a = f.read()
    f.close()
    return a

#-----список алфавита-----
#-----имя файла с алфавитом: alphabet.txt-----
def get_alphabet():
    url = 'http://makedonski.info'
    response = open_page(url)
    #print(response)
    regex = r'<a href="/letter/(.*?)"'
    res = re.findall(regex, response)
    #print(res)
    if res:
        s = ''          # s — имя строки которая потому будет списком букв
        for elem in res:
            s = s + str(elem) + '\n'
        w_in_file('alphabet.txt', s)
        #print(s)
    return res          # я пока не отпределилась но пусть пока возвращает массив с алфавитом
#get_alphabet()

#-----выдаёт слово-слово список в файл чтобы потом открывать-----
def get_alphabet_links():
    alf_arr = get_alphabet()
    def_url = 'http://makedonski.info/letter/'
    url_alf = ''
    for elem in alf_arr:
        url_alf = url_alf + def_url + str(elem) + '\n'
    w_in_file('alphaber_urls.txt', url_alf)     # файл со ссылками, url_alf название массива со ссылками
    alf_links = url_alf.split('\n')
    #print(url_alf)
    #print(alf_links)
    return alf_links

def get_words():
    alf_links = get_alphabet_links()
    #print(open_page(alf_links[1]))
    for elem in alf_links:
        text = open_page(elem)
        regex = r'<option value="/letter/(.*?)"'            #r'<a href="/letter/(.*?)"'
        res = re.findall(regex, text)

        print(res)


get_words()

