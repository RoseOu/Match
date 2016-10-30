# coding: utf-8

from flask import jsonify, url_for,request
from . import app
import urllib
import urllib2
import json
import jieba
import jieba.analyse
from .zhihu import zhihucount
from .weibo import weibocount
from .wangyi import wangyicount
from .douban import doubancount

@app.route('/getScore/', methods=['GET','POST'])
def getScore():
	doubanId1=request.get_json().get("doubanId1")
	wangyiId1=request.get_json().get("wangyiId1")
	weiboId1=request.get_json().get("weiboId1")
	zhihuId1=request.get_json().get("zhihuId1")
	
	doubanId2=request.get_json().get("doubanId2")
	wangyiId2=request.get_json().get("wangyiId2")
	weiboId2=request.get_json().get("weiboId2")
	zhihuId2=request.get_json().get("zhihuId2")

	if doubanId1 and doubanId2:
		doubandata=json.loads(doubancount(doubanId1,doubanId2)[0])
		doubanscore=doubandata["douscore"]
		doubanfilm=doubandata["samefilm"]
		doubanbook=doubandata["samebook"]
	else:
		doubanscore=""
		doubanfilm=""
		doubanbook=""

	if wangyiId1 and wangyiId2:
		wangyiId1.replace(" ","+")
		wangyiId2.replace(" ","+")
		wangyidata=json.loads(wangyicount(wangyiId1,wangyiId2)[0])
		wangyiscore=wangyidata["songscore"]
		wangyisong=wangyidata["samesong"]
	else:
		wangyiscore=""
		wangyisong=""

	if weiboId1 and weiboId2:
		weibodata=json.loads(weibocount(weiboId1,weiboId2)[0])
		weiboscore=weibodata["weiscore"]
		weibokey=weibodata["samekey"]
	else:
		weiboscore=""
		weibokey=""

	if zhihuId1 and zhihuId2:
		zhihudata=json.loads(zhihucount(zhihuId1,zhihuId2)[0])
		zhihuscore=zhihudata["topicscore"]
		zhihutopic=zhihudata["sametopic"]
	else:
		zhihuscore=""
		zhihutopic=""

	scores=[doubanscore,wangyiscore,weiboscore,zhihuscore]
	i=1
	score=0
	for s in scores:
		if s:
			score=score+s
			i=i+1
	score=score/i*10

	if score<=35:
		message='呃，还是可以说上话的吧？'
	elif 35 < score <= 65:
		message='似乎志趣相投呀~'
	else:
		message='也许这就是传说中的心之友？'

	return jsonify({
    			"score": score,
    			"message": message,
    			"info":{
					"douban":{
						"film":doubanfilm,
						"book":doubanbook
					},
       				"wangyi":wangyisong,
       				"weibo":weibokey,
       				"zhihu":zhihutopic,
   				}
			})

