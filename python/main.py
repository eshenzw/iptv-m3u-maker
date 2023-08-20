#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, redirect, url_for, send_from_directory
import threading

import tools
import iptv

class Main (object):
    def __init__ (self) :
        self.T = tools.Tools()

    def scan (self):
        Crawler = iptv.Iptv()
        Crawler.run()

    def site (self):
        web = Flask(__name__)
        resourcePath = '/srv/iptv/http'

        @web.route('/')
        def index():
            return send_from_directory(resourcePath, 'index.html')

        @web.route('/run')
        def run():
            self.T.logger("开始重新抓取", True)
            thread = threading.Thread(target = self.scan, args = (), daemon = True)
            thread.start()

            return redirect(url_for('log'))

        @web.route('/m3u')
        def m3u8():
            return send_from_directory(resourcePath, 'tv.m3u')

        @web.route('/tv.m3u')
        def tvm3u8():
            return send_from_directory(resourcePath, 'tv.m3u')

        @web.route('/json')
        def json():
            return send_from_directory(resourcePath, 'tv.json')

        @web.route('/tv.json')
        def tvjson():
            return send_from_directory(resourcePath, 'tv.json')

        @web.route('/log')
        def log():
            return send_from_directory(resourcePath, 'log.txt')

        self.T.logger("listen on port: 9527", True)
        web.run(
            host = '0.0.0.0',
            port = 9527,
            debug = False
        )

    def run (self):
        threads = []

        thread = threading.Thread(target = self.site, args = (), daemon = True)
        thread.start()
        threads.append(thread)

        self.T.logger("开始抓取", True)
        thread = threading.Thread(target = self.scan, args = (), daemon = True)
        thread.start()
        threads.append(thread)

        for t in threads:
            t.join()

if __name__ == '__main__':
    App = Main()
    App.run()
