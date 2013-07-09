# -*- coding: utf-8 -*-
"""
    user
    ~~~~~~

    使用者資料、管理的功能部份

"""


from flask import Blueprint, render_template, abort, redirect, url_for, flash
from flask import g
from flask import request
from flask import jsonify
#from jinja2 import TemplateNotFound

# 資料庫相關
#from model.extensions import db
#from model.GameObj import DbGame
from model.UserObj import DbUser

# 字典
from dict.yahoo import YahooDict

user = Blueprint('user', __name__)



@user.route('/profile')
@user.route('/profile/<name>')
def profile(name=""):
    '''
    使用者資訊
    '''
    Member_ = g.user
    if name != "":
        Member_ = DbUser.query.filter_by(account=name).first()

    # if g.user == None:
    #     #若不是本人就秀使用者資訊
    #     Member_ = DbUser.query.filter_by(account=name).first()
    #     #articles_ = DbArticle.query.filter_by(member_no=Member_.index)
    #     return render_template('user/Profile.html',Member=Member_)

    #若是本人就秀控制介面
    return render_template('user/Profile.html',Member=Member_)

@user.route('/search')
def search():
    '''查單字頁面'''
    return render_template('user/search.html')


@user.route('/query', methods=['POST'])
def query_word():
    '''查詢單字'''
    # print request.json
    # js = jsonify(**request.json)
    word = request.json['word']

    dict = YahooDict()
    result = dict.query(word)
    if result == None:
        result = "Can't find!"
    return result
