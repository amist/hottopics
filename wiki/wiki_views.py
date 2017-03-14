import requests
import jinja2
from datetime import timedelta, date
from multiprocessing.pool import ThreadPool

class WikiViews(object):
    def __init__(self):
        self.lang = 'en'
        #self.lang = 'he'
        self.access = 'mobile-web'
        #self.access = 'all-access'


    def get_day_stats(self, day):
        cmd = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/{}.wikipedia/{}/{}/{:02d}/{:02d}'.format(self.lang, self.access, day.year, day.month, day.day)
        ret = requests.get(cmd).json()
        return ret


    def get_all_stats(self, date_start, date_end):
        dates = [(date_start + timedelta(n)) for n in range((date_end - date_start).days+1)]
        pool = ThreadPool(50)
        stats = pool.map(self.get_day_stats, dates)
        return stats


    def get_html_stats(self, date_start, date_end):
        templateLoader = jinja2.FileSystemLoader(searchpath=".")
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template("template.html")
        stats = self.get_all_stats(date_start, date_end)
        max_val = max([x['views'] for stat in stats for x in stat['items'][0]['articles']])
        template_vars = {'stats': stats, 'num': 20, 'lang': self.lang, 'max_val': max_val}
        html = template.render(template_vars)
        with open('report.html', 'w', encoding='utf8') as f:
            f.write(html)

        
if __name__ == '__main__':
    wv = WikiViews()
    date_start = date(2015, 7, 1)
    #date_start = date(2017, 3, 10)
    date_end = date(2017, 3, 11)
    wv.get_html_stats(date_start, date_end)

