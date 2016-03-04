#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import queue
import threading
import os
from urllib.request import urlopen,Request
from urllib.error import HTTPError

threads = 10

target = "http://www.example.com/wordpress"
directory = ""

filters = [".jpg",".gif","png",".css"]
web_path = queue.Queue()


for r, d,f in os.walk("."):
    for files in f:
        remote_path = "{!s}/{!s}".format(r,files)
        if remote_path.startswith("."):
            remote_path = remote_path[1:]
        if os.path.splitext(files)[1] not in filters:
            web_path.put(remote_path)

def test_remote():
    while not web_path.empty():
        path = web_path.get()
        url ="{!s}{!s}".format(target, path)
        request = Request(url)
        try:
            responses = urlopen(request)
            content = response.read()

            print("[{:d}] => {!s}".format(response.code, path))
            response.close()
        except HTTPError as error:
            pass

for i  in range(threads):
    print("Spawning thread: {:d}".format(i))
    t = threading.Thread(target=test_remote)
    t.start()
        
