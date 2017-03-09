import requests
import jinja2
from datetime import timedelta, date
from multiprocessing.pool import ThreadPool

class WikiViews(object):
    def __init__(self):
        pass


    def get_day_stats(self, day):
        cmd = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/mobile-web/{}/{:02d}/{:02d}'.format(day.year, day.month, day.day)
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
        template_vars = {'stats': stats, 'num': 20}
        html = template.render(template_vars)
        with open('report.html', 'w', encoding='utf8') as f:
            f.write(html)

        
if __name__ == '__main__':
    wv = WikiViews()
    date_start = date(2016, 1, 1)
    date_end = date(2017, 3, 8)
    wv.get_html_stats(date_start, date_end)

