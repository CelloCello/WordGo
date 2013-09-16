# -*- coding: utf-8 -*-
"""
    word
    ~~~~~~

    單字相關功能

"""

import json
import os
import time, datetime
#import shelve
from flask import Blueprint, render_template, abort, redirect, url_for, flash
from flask import g
from flask import request
from flask import jsonify
#from jinja2 import TemplateNotFound

# 資料庫相關
#from model.extensions import db
#from model.GameObj import DbGame
from pymongo import MongoClient

# 字典
from dict.yahoo import YahooDict


word = Blueprint('word', __name__)



@word.route('/search')
def search():
    '''查單字頁面'''
    return render_template('word/search.html')


@word.route('/query', methods=['POST'])
def query_word():
    '''查詢單字'''
    # print request.json
    # js = jsonify(**request.json)
    word = request.json['word']

    dict = YahooDict()
    result = dict.query(word).html()
    if result == None:
        result = "Can't find!"
    return result

@word.route('/save', methods=['POST'])
def save():
    '''存到單字本(存到mongodb)'''
    
    if g.user == None:
        return "You should login first!"

    word = request.json['word']
    try:  

        mcli = MongoClient('localhost', 27017)
        mdb = mcli.wordgo
        db_words = mdb.word
		
        # 確認是否已經有了
        qword = db_words.find_one({"word" : word })
        print qword
        if qword:
            return "have!!"		
    	
        dict = YahooDict()
        result = dict.query(word)
        word_info = {}
        word_info['html'] = result.html()
        word_info['text'] = result.text()
        
        # json
        t = time.time()
        word_jn = {}
        word_jn['user'] = g.user.account
        word_jn['word'] = word
        word_jn['word_info'] = word_info
        word_jn['familiar'] = 0
        word_jn['date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))

        word_id = db_words.insert(word_jn)
        print word_id
        
    except ValueError:
    	return "Save Error"

    return "Saved"

@word.route('/save_old', methods=['POST'])
def save_old():
    '''存到單字本(舊的, 寫入到本地端資料)'''
    word = request.json['word']
    if g.user:
        fn = "users/"+g.user.account+"/words.dat"
        path = "." + url_for('static', filename=fn)
        #path = ".//static//users//"+g.user.account+"//words.dat"
        print path
        try:  
            dict = YahooDict()
            result = dict.query(word)
            word_info = {}
            word_info['html'] = result.html()
            word_info['text'] = result.text()
            
            # # shelve
            # db = shelve.open(path, 'c')  
            # db[str(word)] = word_info

            if not os.path.exists(path):
                ff = open(path,"w+")
                ff.close()

            # json
            word_jn = {}
            try:
                with open(path,"r") as f: 
                    word_jn = json.load(f)
            except ValueError:
                pass

            word_jn[word] = word_info
            f = open(path,"w")
            json.dump(word_jn,f)

        finally:  
            #db.close()
            f.close()

    return "Saved"

@word.route('/book')
def book():
    '''打開單字本(mongodb)'''
    if g.user == None:
        flash("You should login first!")
        return redirect(url_for('index'))

	
    words = {}
    try:  
    
        mcli = MongoClient('localhost', 27017)
        mdb = mcli.wordgo
        db_words = mdb.word

        words = db_words.find()
        
    finally:  
        pass
        #words.close()

    #print words.count()
    return render_template('word/wordbook.html',words=words)

@word.route('/wordbook_old')
def wordbook_old():
    '''打開單字本(舊的, 呼叫本地端資料用)'''
    if g.user == None:
        return url_for('index')

    fn = "users/"+g.user.account+"/words.dat"
    path = "." + url_for('static', filename=fn)
    print path
    #path = ".//static//users//"+g.user.account+"//words.dat"
    words = {}
    try:  
        #words = shelve.open(path, 'c') 

        if not os.path.exists(path):
            ff = open(path,"w+")
            ff.close()

        try:
            with open(path,"r") as f: 
                words = json.load(f)
        except ValueError:
            pass
        
    finally:  
        pass
        #words.close()

    print len(words)
    return render_template('user/wordbook.html',words=words)

@word.route('/delete/<word>', methods=['POST'])
def delete(word):
    '''刪除單字(mongodb)'''

    if g.user == None:
        flash("You should login first!")
        return redirect(url_for('index'))

    try:
    	mcli = MongoClient('localhost', 27017)
    	mdb = mcli.wordgo
    	db_words = mdb.word
    	db_words.remove({"user" : g.user.account, "word" : word})
        
    finally:  
    	pass

    return "remove ok"


@word.route('/show/<word>', methods=['POST', 'GET'])
def show(word):
    '''顯示單字本的單字'''
    if g.user == None:
        flash("You should login first!")
        return redirect(url_for('index'))

    mcli = MongoClient('localhost', 27017)
    mdb = mcli.wordgo
    db_words = mdb.word
    qword = db_words.find_one({"word" : word})
    return render_template('word/show.html',qword=qword)