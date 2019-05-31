# !/usr/bin/python3.6
# -*- coding:utf-8 -*-
'''
Project: toutiaoSpider
Author: jc feng (jcfeng2013@gmail.com)
File Created: 2019-05-31 17:19:34
Last Modified: 2019-05-31 21:16:11
'''

import re
import time
from html.parser import HTMLParser
from common.save import SaveTool
from common.http import HttpTool
from common.url import UrlTool
from common.base import create_folder, create_path
from common.utils import secure_string
from api import PC_FEED_API, BASE_URL

folder = 'html'


def get_feed_news(max_behot_time, sleep=1):
    result, status_code = HttpTool.get(url=PC_FEED_API, params={'max_behot_time': max_behot_time}, headers=UrlTool.randomHeaders(), retFormat='json')
    for news in result['data']:
        news_url = BASE_URL + 'a' + news['group_id']
        text, status = HttpTool.get(url=news_url, headers=UrlTool.randomHeaders(), retFormat='text')
        time.sleep(sleep)
        if status == 200:
            try:
                title, content, source, source_time = extract_news_text(text)
            except:
                print(news_url)
                continue
            filename = secure_string(f'{title}_{source}_{source_time}.html')
            filename = create_path(folder, filename)
            SaveTool.saveText(content, filename)
            print(f'{filename} save success')
        else:
            print(news_url)
    get_feed_news(result['next']['max_behot_time'])


def extract_news_text(text):
    content = re.findall(r"content: '(.*)',", text)[0]
    title = re.findall(r"title: '(.*)',", text)[0]
    source = re.findall(r"source: '(.*)',", text)
    source = source[0] if source else 'unknown'
    time = re.search(r"time: '(.*)'", text).group(1)
    content = HTMLParser().unescape(content)
    return title, content, source, time


if __name__ == "__main__":
    create_folder(folder)
    get_feed_news(int(time.time()), sleep=1)
