# coding: utf-8

from flask import jsonify
from . import app
import urllib
import urllib2
import json
from lxml import etree
import jieba


@app.route('/weibo/<user>', methods=['GET','POST'])
def weibo(user):
	
	header = {
		"Accept":"*/*",
		"Connection":"keep-alive",
	    "Cookie": "_T_WM=e67f7f47d7a164548f2218faaf008f70; SCF=AodVtVkaxjeEs8cBpbNbiNBw8dIkjIFhz5qNSnvi3Y2wfmhvbiWyRKFgnNmqVwDNeEvJCIswQJ31k46o-LPLGGQ.; SUHB=00x5VUHUDsIQsR; WEIBOCN_FROM=feed; gsid_CTandWM=4ugyfaa31O5PS4HNlfFxfd0ZL6l; SUB=_2A251EBMgDeTxGeVP61AR-S3Pwj-IHXVW-r1orDV6PUJbkdANLUnFkW0fqGoxURZzjLpek4t2QhbqCgdIuQ..",
		"Host":"weibo.cn",
		"Referer":"http://weibo.cn/",
		"User-Agent":"Chrome/53.0.2785.143"
	    }	

	searchurl="http://weibo.cn/search/?tf=5_012&vt=4"
	searchvalues = {
	"keyword":user,
	"suser":"找人"
	}
	searchdata = urllib.urlencode(searchvalues)
	searchrequest=urllib2.Request(searchurl,searchdata,headers=header)
	searchresponse=urllib2.urlopen(searchrequest)
	searchpage=searchresponse.read()
	sSelector = etree.HTML(searchpage)
	weibolist=[]

	try:
		userurl=sSelector.xpath('//table')[0].xpath('tr/td')[0].xpath('a/@href')[0]
		wholeurl=''.join(["http://weibo.cn",userurl])

		focusrequest=urllib2.Request(wholeurl,headers=header)
		focusresponse=urllib2.urlopen(focusrequest)
		focuspage=focusresponse.read()
		fSelector = etree.HTML(focuspage)
		focusurl=fSelector.xpath('//div[@class="tip2"]/a')[0].xpath('@href')[0]

		i=1
		while i<=10:
			url=''.join(["http://weibo.cn",focusurl,"&page=",str(i)])
			request=urllib2.Request(url, headers=header)
			response=urllib2.urlopen(request)
			page=response.read()
			Selector = etree.HTML(page)
			content=Selector.xpath('//table')
			for each in content:
				weibo=each.xpath('tr/td[@valign="top"]')[1].xpath('a')[0].xpath('text()')[0]
				weibolist.append(weibo)
			i=i+1
			pagenum=Selector.xpath('//div[@class="pa"]/form/div/a/text()')
			if u"下页" in pagenum:
				pass
			else:
				break
	except IndexError:
		pass

	return json.dumps({
		'weibos':weibolist,
		}),{'Content-Type': 'application/json'}

@app.route('/weibocount/<user1>/<user2>', methods=['GET','POST'])
def weibocount(user1,user2):
	samenum=0.0
	samekeys=[]
	weibos1=json.loads(weibo(user1)[0])['weibos']
	weibos2=json.loads(weibo(user2)[0])['weibos']
	keynum1=len(weibos1)
	keynum2=len(weibos2)
	for key in weibos1:
		if key in weibos2:
			if key not in samekeys:
				samenum=samenum+1
				samekeys.append(key)
	samekey=','.join(samekeys)
	if keynum1==0 or keynum2==0:
		weiscore=0
	else:
		weiscore=(samenum/keynum1+samenum/keynum2)/2*100
	return json.dumps({
		'samekey':samekey,
		'weiscore':weiscore
		}),{'Content-Type': 'application/json'}


