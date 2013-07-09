# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq

# q = pq(url='http://tw.dictionary.yahoo.com/dictionary?p=sss&tab1=definition', parser='html')
# word_scope = q('.result_cluster_first')

# print word_scope.html()

class Word:
    '''一個字'''
    title = ""          # 字
    pronounce = ""      # 發音
    explanation = ""    # 解釋
    sentence = ""       # 例句
    pass


# word = Word()
# word.title = word_scope.find('.yschttl').text()
# word.pronounce = word_scope.find('.proun_wrapper').text()
# word.explanation = word_scope.find('.explanation_wrapper').text()
# aaa = word_scope.find('.explanation_wrapper').find('.explanation_pos_wrapper')
# print len(aaa)
# for exp in aaa:
#     print pq(exp).text()
#     print '----'
# print word_scope.find('.explanation_wrapper').find('.explanation_pos_wrapper').eq(1).html()
# #print word.title
# #print word.pronounce
# #print word.explanation

class YahooDict:
    '''Yahoo dictionary'''

    def query(self, word):
        query_url = "http://tw.dictionary.yahoo.com/dictionary?p=%s&tab1=definition" % word.encode('utf-8')
        #print query_url
        q = pq(url=query_url, parser='html')
        word_scope = q('.result_cluster_first')
        return word_scope.find('.explanation_wrapper').html()
