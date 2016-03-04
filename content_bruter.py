#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import queue
import threading
import os
from urllib.request import urlopen,Request
from urllib.error import HTTPError, URLError
from urllib.parse import quote 
threads = 50

target_url = "http://www.example.com"
wordlist_file = "all.txt"
resume = None
user_agent = b"Mozilla/5.0 (x11; Linux x86_64; rv:19.0) \
Gecko/20100101Firefox/19.0"


    
    
def build_wordlist(wordlist_file):
    fd = open(wordlist_file,"rb")
    raw_words = fd.readlines()
    fd.close()

    found_resume = False
    words = queue.Queue()
    for word in raw_words:
        word = word.rstrip()
        if resume is not None:
            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print("Resuming wordlist from: {!s}".resume)
        else:
            words.put(word)
    return words
                    
def dir_bruter(word_queue, extentions=None):

    while not word_queue.empty():
        attempt  = word_queue.get()
        attempt_list = []

        if b"."  not in attempt:
            attempt_list.append("/{!s}/".format(attempt))
        else:
            attempt_list.append("/{!s}".format(attempt))
        if extentions:
            for extention in extentions:
                attempt_list.append("/{!s}{!s}".format(attempt,extention))
        for brute in attempt_list:
            url = "{!s}{!s}".format(target_url,quote(brute))
            try:
                headers = {}
                headers["User-Agent"] = user_agent
                r = Request(url,headers=headers)

                response = urlopen(r)

                if len(response.read()):
                    print("[{:d}] => {!s}".format(response.code, url))
            except URLError as e:
                if hasattr(e, 'code') and e.code != 404:
                    print("!!! {:d} => {!s}".format(e.code, url))
                pass
            

word_queue = build_wordlist(wordlist_file)
extentions = [".php",".bak","org",".inc"]

for i  in range(threads):
    t = threading.Thread(target=dir_bruter, args=(word_queue, extentions))
    t.start()
    
