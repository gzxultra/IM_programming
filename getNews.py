from datetime import  datetime
import feedparser
NEWS_FEED_URL = 'http://news.163.com/special/00011K6L/%s.xml'

def read_news(feed_url):
	try:
		data = feedparser.parse(feed_url)
	except Exception, e:
		print "Got error:%s" %str(e)

	for entry in data.entries:
		print(entry.title)
		print(entry.link)
		print(entry.description)
		print("\n")

if __name__ =='__main__':
	print "==== Reading technology news feed (%s)====" %datetime.today()
	print "Enter the type of news feed: "
	print "Available options are: ?"
	type = raw_input("News feed type: ")
	read_news(NEWS_FEED_URL %type)
	print "==== End of news feed ===="