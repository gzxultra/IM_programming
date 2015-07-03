# -*- coding: utf-8 -*-
from datetime import  datetime
import feedparser
NEWS_FEED_URL = 'http://www.chinanews.com/rss/%s.xml'
dict ={"即时新闻" :"scroll-news","要闻导读" :"importnews","国内新闻" :"china","国际新闻" :"world",
"军事新闻" :"mil","社会新闻" :"society","港澳新闻" :"gangao","台湾新闻" :"taiwan",
"华人新闻" :"chinese","财经新闻" :"finance","文化新闻" :"culture","理论新闻" :"theory","娱乐新闻" :"ent","体育新闻" :"sports",
"教育新闻" :"sports","健康新闻" :"health","IT新闻" :"health","房产新闻" :"estate","汽车新闻" :"auto","图片新闻" :"photo","视频新闻" :"photo",
"法治新闻" :"photo","金融新闻" :"fortune","证券新闻" :"stock","侨界新闻" :"zgqj","华教新闻" :"hwjy","地方新闻" :"df","能源新闻" :"energy",
"生活新闻" :"life","葡萄酒新闻" :"wine","留学生活" :"lxsh","侨乡传真" :"qxcz"}

def read_news(feed_url):
	try:
		data = feedparser.parse(feed_url)
	except Exception, e:
		print "Got error:%s" %str(e)

	if len(data.entries) == 0:
		print "暂无新闻"
	else:
		for entry in data.entries:
			print(entry.title)
			print(entry.link)
			print(entry.description)
			print("\n")

if __name__ =='__main__':
	print "==== Reading technology news feed (%s)====" % datetime.today()
	print "Enter the type of news feed: "
	print "Available options are: 即时新闻,要闻导读,国内新闻,国际新闻,军事新闻,社会新闻,港澳新闻,",
	print "台湾新闻,华人新闻,财经新闻,文化新闻,理论新闻,娱乐新闻,体育新闻,教育新闻,健康新闻,",
	print "IT 新闻,房产新闻,汽车新闻,图片新闻,视频新闻,法治新闻,金融新闻,证券新闻,侨界新闻,",
	print "华教新闻,地方新闻,能源新闻,生活新闻,葡萄酒新闻,留学生活,侨乡传真"
	type = dict[raw_input("News feed type: ")]
	read_news(NEWS_FEED_URL %type)
	print "==== End of news feed ===="