import sys
import requests

def get_top():
    return requests.get('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty').json()
    
    
def get_item(item):
    return requests.get('https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty'.format(item)).json()
    
    
def get_stats():
    stats = {}
    data = get_top()
    for i, item in enumerate(data):
        new_item = get_item(item)
        if new_item['type'] == 'job':
            continue
        if 'id' not in new_item or 'descendants' not in new_item or 'title' not in new_item:
            print('KeyError', file=sys.stderr)
            print(new_item, file=sys.stderr)
        else:
            stats[item] = new_item
            
#            trends = [[x['id'], x['descendants']] for x in stats.values()]
#            trends.sort(key = lambda x: -x[1])
#            print('{}/{} - {}'.format(i, len(data), trends[:6]), file=sys.stderr)
        print('{}%           '.format(100*i/len(data)), end='\r', file=sys.stderr)
    return stats
        
        
def main():
    stats = get_stats()
#    print(stats)
    data = [[x['id'], x['descendants'], x['title'], x.get('url', '')] for x in stats.values()]
    data.sort(key=lambda x: -x[1])
    for item in data:
        try:
            print('{} - {}\n{}\n'.format(item[1], item[2], item[3]))
        except UnicodeEncodeError:
            print('{}\n{}\n'.format(item[1], item[3]))
    
    

if __name__ == '__main__':
    main()