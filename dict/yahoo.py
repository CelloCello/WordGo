# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq

q = pq(url='http://tw.dictionary.yahoo.com/dictionary?p=apple&tab1=definition', parser='html')
print q('.result_cluster_first').text()

class Word:
    '''一個字'''
    title = ""          # 字
    pronounce = ""      # 發音
    explanation = ""    # 解釋
    sentence = ""       # 例句
    pass

class YahooDict:
    '''Yahoo dictionary'''


    def search(word):
        pass
