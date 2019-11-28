import feedparser
from time import mktime
from datetime import datetime
from newspaper import Article
import dateutil.parser as dparser


class Reader(object):
    'class for reading RSS-feeds'

    def __init__(self, site):
        self.site = site
        
    def get_feed(self):
        d = feedparser.parse(self.site)
        return d['entries']
    def state(self):
        d = feedparser.parse(self.site)
        status=d.status
        print("Status:{}".format(status))
    def read_news(self, limit):
        count=1
        news=[]
        f = self.get_feed()
        for entry in f:
            # Check if publish date is provided, if no the article is skipped.
            if hasattr(entry, 'published'):
                if count > limit:
                    break
                article = {}
                article['link'] = entry.link
                date = entry.published_parsed
                article['published'] = datetime.fromtimestamp(mktime(date)).isoformat()
                
                try:
                    content = Article(entry.link)
                    content.download()
                    content.parse()
                except Exception as e:
                    # If the download for some reason fails (ex. 404) the script will continue downloading
                    # the next article.
                    print(e)
                    print("continuing...")
                    continue
                article['title'] = content.title
                article['text'] = content.text                 
                print(article)
                news.append(article)
                with open('rss.txt', 'w') as f:
                     for article in news:
                         f.write("%s\n" % article)
                count +=1
                
    def date(self, limit, data):
        #Looks for the news on a certain date.
        count=1
        news=[]
        f = self.get_feed()
        filtered_f=[entry for entry in f if datetime.strftime(dparser.parse(entry.published,fuzzy=True), '%Y%m%d')\
                    ==datetime.strftime(data, '%Y%m%d')]
        for entry in filtered_f:
                if count > limit:
                    break
                article = {}
                article['link'] = entry.link
                date = entry.published_parsed
                article['published'] = datetime.fromtimestamp(mktime(date)).isoformat()
                
                try:
                    content = Article(entry.link)
                    content.download()
                    content.parse()
                except Exception as e:
                    print(e)
                    print("continuing...")
                    continue
                article['title'] = content.title
                article['text'] = content.text                 
                print(article)
                news.append(article)
                with open('rss.txt', 'w') as f:
                     for article in news:
                         f.write("%s\n" % article)
                count +=1

    
          

