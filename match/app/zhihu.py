# coding: utf-8

from flask import jsonify
from . import app
import urllib
import urllib2
import json
from lxml import etree

@app.route('/zhihu/<user>', methods=['GET','POST'])
def zhihu(user):
	header = {
		"Accept":"*/*",
		"Connection":"keep-alive",
		"Content-Type":"application/x-www-form-urlencoded",
        "cookie": 'd_c0="AHDA5wX1OAqPTpRl9RPevO-j5smR_Spex2Q=|1468401019"; _za=3a696b8c-b203-4f70-b271-bc6d35f942e6; _zap=b1962b44-4f90-4e3a-bcce-97ae28b46a72; _xsrf=8d63f2a175b108000bdac51f2e5bc94f; l_cap_id="MjRjOTM5MjJjN2ZkNGQwYmE1NzY3ZjIzMGRmOTYxOGE=|1477128678|63b5e53a3b7ee60a1e4f92e7eb9198830d442bed"; cap_id="NWIzNDQ5NTBiOTE4NDdlMDlmN2E0NDA0MDhlYjUyYzk=|1477128678|186344adbb2800f2b58be3ef80fb3ffeb945b248"; login="ODdhZjgzNTQzNjFhNDk3YzhjMTgzNDUyOTI2YWY1YTI=|1477128715|8b74d9700ab36b33845c5e83ef6378ae3c59ed0e"; q_c1=91f5b2672db44abfb2d1449830eb2bac|1477277836000|1468401019000; s-q=s; s-i=1; sid=26bkipf8; a_t="2.0AADANlJDqwkXAAAAv5Y7WAAAwDZSQ6sJAHDA5wX1OAoXAAAAYQJVTQu_MlgAzRpR6JPNIp6lcWqzZT_Iqe4G_8RA_a2nQH5N4x2WuK2m3nNgy5aZPg=="; z_c0=Mi4wQUFEQU5sSkRxd2tBY01EbkJmVTRDaGNBQUFCaEFsVk5DNzh5V0FETkdsSG9rODBpbnFWeGFyTmxQOGlwN2diX3hB|1477708223|6960a48c07141eeedd29c49c37a13b918f2458b0; __utma=51854390.962657604.1477487059.1477705250.1477708226.9; __utmc=51854390; __utmz=51854390.1477705250.8.8.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/search; __utmv=51854390.100--|2=registration_date=20160325=1^3=entry_date=20160325=1',
		"Host":"www.zhihu.com",
		"User-Agent":"Chrome/53.0.2785.143"
        }

	user = urllib.quote(user.encode('utf8'))
	searchurl="https://www.zhihu.com/search?type=people&q="+user
	searchrequest=urllib2.Request(searchurl)
	searchresponse=urllib2.urlopen(searchrequest)
	searchpage=searchresponse.read()
	Selector = etree.HTML(searchpage)
	topiclist=[]
	try:
		userurl=Selector.xpath('//div[@class="line"]')[0].xpath('a')[0].xpath('@href')[0]
		url = ''.join(["https://www.zhihu.com",userurl,"/topics"])
		request=urllib2.Request(url, headers=header)
		response=urllib2.urlopen(request)
		page=response.read()
		Selector = etree.HTML(page)
		content=Selector.xpath('//div[@class="zm-profile-section-main"]')
		for each in content:
			topic=each.xpath('a[starts-with(@href,"/topic")]/strong/text()')[0]
			topiclist.append(topic)
	except IndexError:
		pass

	return json.dumps({
		'topics':topiclist,
		}),{'Content-Type': 'application/json'}


@app.route('/zhihucount/<user1>/<user2>', methods=['GET','POST'])
def zhihucount(user1,user2):
	samenum=0.0
	topicnum1=0.0
	topicnum2=0.0
	sametopics=[]
	topics1=json.loads(zhihu(user1)[0])['topics']
	topics2=json.loads(zhihu(user2)[0])['topics']
	topicnum1=len(topics1)
	topicnum2=len(topics2)
	for topic in topics1:
		if topic in topics2:
			if topic not in sametopics:
				samenum=samenum+1
				sametopics.append(topic)
	sametopic=', '.join(sametopics)
	if topicnum1==0 or topicnum2 ==0:
		topicscore=0
	else:
		topicscore=(samenum/topicnum1+samenum/topicnum2)/2*100
	return json.dumps({
		'sametopic':sametopic,
		'topicscore':topicscore,
		}),{'Content-Type': 'application/json'}
