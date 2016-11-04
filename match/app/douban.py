# coding: utf-8

from flask import jsonify
from . import app
import urllib
import urllib2
import json
from lxml import etree


@app.route('/douban/<user>', methods=['GET','POST'])
def douban(user):
	cookie='bid=gtzg1DNOTGQ; gr_user_id=f7b80669-7393-4162-a457-b48566420845; ll="118254"; ps=y; _vwo_uuid_v2=91885013FF717C8E1AC687B90797D35D|3e0a91b8e6d93c5ba2ef2d40cc4d8e9e; ct=y; ue="598959770@qq.com"; dbcl2="153124327:rkg6xlUEjmc"; ck=p9on; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1477738358%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DR32BSv1_3xwf6ZJhCc7PNUqln_FVX7PClWrB1mdkH4y%26wd%3D%26eqid%3Dd039a4e000064d2d00000005581435d9%22%5D; push_noty_num=0; push_doumail_num=0; _pk_id.100001.8cb4=53e82647b1b897e3.1468064329.23.1477738811.1477735250.; _pk_ses.100001.8cb4=*; __utma=30149280.2087076758.1468064331.1477720025.1477734544.21; __utmb=30149280.28.10.1477734544; __utmc=30149280; __utmz=30149280.1477720025.20.16.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.15312; ap=1'
	searchheader = {
		"Accept":"*/*",
		"Connection":"keep-alive",
	    	"cookie":cookie,
		"Host":"www.douban.com",
		"User-Agent":"Chrome/53.0.2785.143"
	    }
	filmheader = {
		"Accept":"*/*",
		"Connection":"keep-alive",
	    	"cookie":cookie,
		"Host":"movie.douban.com",
		"User-Agent":"Chrome/53.0.2785.143"
	    }
	bookheader = {
		"Accept":"*/*",
		"Connection":"keep-alive",
	   	"cookie":cookie,
		"Host":"book.douban.com",
		"User-Agent":"Chrome/53.0.2785.143"
	    }

	# '''user1'''

	# #get user id
	user = urllib.quote(user.encode('utf8'))
	searchurl="https://www.douban.com/search?cat=1005&q="+user
	searchrequest=urllib2.Request(searchurl,headers=searchheader)
	searchresponse=urllib2.urlopen(searchrequest)
	searchpage=searchresponse.read()
	Selector = etree.HTML(searchpage)
	filmlist=[]
	booklist=[]

	try:
		userurl=Selector.xpath('//div[@class="result-list"]/div[@class="result"]')[0].xpath('div[@class="pic"]/a/@href')[0]
		userid=userurl.split('%2F')[4]

	#get user film
		fstart=0
		while 1:
			filmurl=''.join(["https://movie.douban.com/people/",userid,"/collect","?start=",str(fstart),"&sort=time&rating=all&filter=all&mode=grid"])
			filmrequest=urllib2.Request(filmurl,headers=filmheader)
			filmresponse=urllib2.urlopen(filmrequest)
			filmpage=filmresponse.read()
			filmSelector = etree.HTML(filmpage)
			filmcontent=filmSelector.xpath('//div[@class="grid-view"]/div[@class="item"]')
			for filmeach in filmcontent:
				film=filmeach.xpath('div[@class="info"]/ul/li[@class="title"]/a/em/text()')[0]
				if film not in filmlist:
					filmlist.append(film)
			fstart=fstart+15
			filmpagenum=filmSelector.xpath('//div[@class="paginator"]/span[@class="next"]/a')
			if filmpagenum:
				pass
			else:
				break

	#get user book
		bstart=0
		while 1:
			bookurl=''.join(["https://book.douban.com/people/",userid,"/collect","?start=",str(bstart),"&sort=time&rating=all&filter=all&mode=grid"])
			bookrequest=urllib2.Request(bookurl,headers=bookheader)
			bookresponse=urllib2.urlopen(bookrequest)
			bookpage=bookresponse.read()
			bookSelector = etree.HTML(bookpage)
			bookcontent=bookSelector.xpath('//ul[@class="interest-list"]/li[@class="subject-item"]')
			for bookeach in bookcontent:
				book=bookeach.xpath('div[@class="info"]/h2/a/@title')[0]
				if book not in booklist:
					booklist.append(book)
			bstart=bstart+15
			bookpagenum=bookSelector.xpath('//div[@class="paginator"]/span[@class="next"]/a')
			if bookpagenum:
				pass
			else:
				break	
	except IndexError:
		pass
	return json.dumps({
			"films":filmlist,
			"books":booklist,
		}),{'Content-Type': 'application/json'}

@app.route('/doubancount/<user1>/<user2>', methods=['GET','POST'])
def doubancount(user1,user2):
	samefilmnum=0.0
	filmnum1=0.0
	filmnum2=0.0
	samefilms=[]
	films1=json.loads(douban(user1)[0])['films']
	films2=json.loads(douban(user2)[0])['films']
	filmnum1=len(films1)
	filmnum2=len(films2)

	for film in films1:
		if film in films2:
			if film not in samefilms:
				samefilmnum=samefilmnum+1
				samefilms.append(film)
	samefilm=', '.join(samefilms)
	if filmnum1==0 or filmnum2 ==0:
		filmscore=0
	else:
		filmscore=(samefilmnum/filmnum1+samefilmnum/filmnum2)/2*100

	samebooknum=0.0
	booknum1=0.0
	booknum2=0.0
	samebooks=[]
	books1=json.loads(douban(user1)[0])['books']
	books2=json.loads(douban(user2)[0])['books']
	booknum1=len(books1)
	booknum2=len(books2)

	for book in books1:
		if book in books2:
			if book not in samebooks:
				samebooknum=samebooknum+1
				samebooks.append(book)
	samebook=','.join(samebooks)
	if booknum1==0 or booknum2 ==0:
		bookscore=0
	else:
		bookscore=(samebooknum/booknum1+samebooknum/booknum2)/2*100

	douscore=0.0
	douscore=(filmscore+bookscore)/2

	return json.dumps({
		'samefilm':samefilm,
		'samebook':samebook,
		'douscore':filmscore,
		}),{'Content-Type': 'application/json'}
