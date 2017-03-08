import sys
import requests
from multiprocessing.pool import ThreadPool
from multiprocessing import Manager

class HNFetch(object):
    def __init__(self):
        self.posts_number = -1
        self.posts_completed = 0
        self.lock = Manager().Lock()
        
        
    def update_progress(self):
        self.lock.acquire()
        self.posts_completed += 1
        print('{}%           '.format(100*self.posts_completed/self.posts_number), end='\r', file=sys.stderr)
        self.lock.release()
    
    
    def get_top(self):
        return requests.get('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty').json()
        
        
    def get_item(self, item):
        # print('fetching item {}'.format(item), file=sys.stderr)
        ret = requests.get('https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty'.format(item)).json()
        self.update_progress()
        return ret
        
        
    def get_stats(self):
        data = self.get_top()
        self.posts_number = len(data)
        
        pool = ThreadPool(50)
        items = pool.map(self.get_item, data)
        pool.close()
        pool.join()
        
        stats = {}
        for item in items:
            if item['type'] == 'job':
                continue
            if 'id' not in item or 'descendants' not in item or 'title' not in item:
                print('KeyError', file=sys.stderr)
                print(item, file=sys.stderr)
            else:
                stats[item['id']] = item
        return stats
            
            
    def fetch(self):
        stats = self.get_stats()
        
        data = [[x['id'], x['descendants'], x['title'], x.get('url', '')] for x in stats.values()]
        data.sort(key=lambda x: -x[1])
        for item in data:
            try:
                print('{} - {}\n{}\n'.format(item[1], item[2], item[3]))
            except UnicodeEncodeError:
                print('{}\n{}\n'.format(item[1], item[3]))
    
    

if __name__ == '__main__':
    hnf = HNFetch()
    hnf.fetch()