import sys
import requests
from multiprocessing.pool import ThreadPool
from multiprocessing import Manager

class RedditFetch(object):
    def __init__(self):
        pass
        
        
    def get_item(self, item):
        ret = requests.get('https://www.reddit.com/r/{}/top/.json?count=20'.format(item), headers = {'User-agent': 'your bot 0.1'}).json()
        return ret
        
        
    def get_items(self):
        #data = ['worldnews', 'reddit.com', 'gadgets', 'gadgets', 'news', 'todayilearned']
        data = ['worldnews', 'gadgets', 'gadgets', 'news', 'todayilearned']
        pool = ThreadPool(50)
        items = pool.map(self.get_item, data)
        pool.close()
        pool.join()
        
        items = [i['data']['children'] for i in items]  # concatenate subreddits items
        items = [i['data'] for o in items for i in o]   # concatenate inner lists
        return items
            
            
    def fetch(self):
        items = self.get_items()
        
        data = [[x['permalink'], x['score'], x['title'], x['url']] for x in items]
        data.sort(key=lambda x: -x[1])
        for item in data:
            print('{} - {}\n{}\n{}\n'.format(item[1], item[0], item[2], item[3]))
    

if __name__ == '__main__':
    f = RedditFetch()
    f.fetch()
