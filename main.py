#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :main.py
@说明        :爬取题库
@时间        :2020/12/13 16:04:22
@作者        :Yanghaa
@版本        :1.0
'''
import requests
from bs4 import BeautifulSoup
import json
import re

Special = 'http://124731.cn/post/390.html'
Weekly = 'http://124731.cn/post/391.html'


def RequestSource(url):
    """
    docstring
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException as identifier:
        return None


def HtmlAnalysis(htmlText, tiType):
    """
    docstring
    """
    topic = []
    soup = BeautifulSoup(htmlText, 'lxml')
    topicList = soup.find_all(["h4", "p"])
    # tiku = {"topic": "", "options": []}
    tikuAll = []
    if tiType == 'special':
        tiNumber = 10
        fileName = './special.json'
    elif tiType == 'weekly':
        tiNumber = 5
        fileName = './weekly.json'
    tikuFile = open(fileName, "w", encoding='utf8')
    for item in topicList:
        tagText = item.text.strip('\n')
        tagText = tagText.strip("\r\n")
        tagText = tagText.strip()
        pattern = re.compile('第[0-9]*期、')
        if pattern.search(tagText) is not None:
            tiku = {"topic": "", "options": []}
            tiku['topic'] = pattern.sub("", tagText)
            answer = []
        pattern = re.compile('^[1-9]\\d*.')
        if pattern.search(tagText) is not None:
            strans = re.sub(" \xa0 复制", "", pattern.sub("", tagText))
            strans = re.sub(" \xa0复制", "", strans)
            answer.append(strans)
            pattern = re.compile(str(tiNumber)+'.')
            if pattern.search(tagText) is not None:
                tiku['options'] = answer
                tikuAll.append(tiku)
    json.dump(tikuAll,tikuFile,indent=6,ensure_ascii=False)
    tikuFile.close()

def main():
    """
    docstring
    """
    a = RequestSource(Special)
    b = HtmlAnalysis(a,'special')
    c = RequestSource(Weekly)
    d = HtmlAnalysis(c,'weekly')
    
if __name__ == "__main__":
    main()
