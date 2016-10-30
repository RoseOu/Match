# coding: utf-8

from flask import jsonify
from . import app
import urllib
import urllib2
import json
from lxml import etree

@app.route('/wangyi/<user>', methods=['GET','POST'])
def wangyi(user):
	header = {
		"Accept":"*/*",
		"Connection":"keep-alive",
		"Cookie":'__gads=ID=087c1cff2a326960:T=1469617037:S=ALNI_Ma7UEsIKmKpKf1iglhxzQ3YzybWtQ; vjuids=7d871f580.1562c0068d3.0.3943cd8314ff3; _ntes_nnid=7df1a897e227f6f9b002685b0df7c247,1469617039595; _ntes_nuid=7df1a897e227f6f9b002685b0df7c247; usertrack=c+5+hleppPhzJSCsAxefAg==; vjlast=1469617040.1474544398.12; vinfo_n_f_l_n3=0e75eb2e60064e26.1.2.1469617039668.1474447179653.1474544442026; Province=027; City=027; _ga=GA1.2.206494557.1470735610; NETEASE_WDA_UID=350197177#|#1477120763991; NTESmusic_yyrSI=51D723D85CDEB48D21866C888EA85F31.classa-music-yyr3.server.163.org-8010; JSESSIONID-WYYY=7ec49d3a264a05f5e927803de840c41ced5c57d89cb616e7bde24c0305b6fd60628f7543347a3319cd86feac15fd5e7d6dd7dfd8414a53c6b1179f7e2af73bd75a47337a8f2c75ed6f64f768072c1ef2fbd459295dddf40e4e4f59b2bfb86b78fb7e3d211f10ed5292700f5f3fe38a7e07fec7953e1dd023481a934bcd03ee5b0d4b9cc1%3A1477532939539; _iuqxldmzr_=25; MUSIC_U=f28f97c83fd5c56c27bba3eb834b86668f8722d719f64f27163c5b087facc07a8e6c76c08b9c185d320dd5100bfb8a5c31b299d667364ed3; __csrf=446f0477161fdabb1214e45de56101ca; __remember_me=true; __utma=94650624.206494557.1470735610.1477488920.1477529393.17; __utmb=94650624.21.10.1477529393; __utmc=94650624; __utmz=94650624.1477402092.12.7.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
		"Referer":"http://music.163.com/",
		"User-Agent":"Chrome/53.0.2785.143",
	}

	#get user id
	searchurl="http://music.163.com/api/search/get/web"
	values = {
	    's': user,
	    'type': '1002',
	    'offset': '0',
	    'limit': '10',
	    }
	data = urllib.urlencode(values)
	searchrequest=urllib2.Request(searchurl,data,header)
	searchresponse=urllib2.urlopen(searchrequest)
	searchcontent=searchresponse.read()
	searchpage=json.loads(searchcontent) 
	songlist=[]
	try:	
		userid=searchpage["result"]["userprofiles"][0]["userId"]

	#get playlist id
		plaurl='http://music.163.com/api/user/playlist/?offset={}&limit={}&uid={}'.format(0, 10, userid)
		plarequest=urllib2.Request(plaurl)
		plaresponse=urllib2.urlopen(plarequest)
		placontent=plaresponse.read()
		plapage=json.loads(placontent) 
		playlistid=plapage["playlist"][0]["id"]

	#catch the songs
		url=''.join(["http://music.163.com/playlist?id=",str(playlistid)])
		request=urllib2.Request(url)
		response=urllib2.urlopen(request)
		page=response.read()
		Selector=etree.HTML(page)
		content=Selector.xpath('//ul[@class="f-hide"]/li')
		for each in content:
			song=each.xpath('a/text()')[0]
			songlist.append(song)
	except IndexError:
		pass
	return json.dumps({
		'songs':songlist,
		}),{'Content-Type': 'application/json'}

@app.route('/wangyicount/<user1>/<user2>', methods=['GET','POST'])
def wangyicount(user1,user2):
	samenum=0.0
	samesongs=[]
	songs1=json.loads(wangyi(user1)[0])['songs']
	songs2=json.loads(wangyi(user2)[0])['songs']
	songnum1=len(songs1)
	songnum2=len(songs2)
	for song in songs1:
		if song in songs2:
			if song not in samesongs:
				samenum=samenum+1
				samesongs.append(song)
	samesong=', '.join(samesongs)
	if songnum1==0 or songnum2==0:
		songscore=0
	else:
		songscore=(samenum/songnum1+samenum/songnum2)/2*100
	return json.dumps({
		'songscore':songscore,
		'samesong':samesong,
		}),{'Content-Type': 'application/json'}

