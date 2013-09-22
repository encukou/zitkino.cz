# -*- coding: utf-8 -*-


import datetime

from zitkino import parsers
from zitkino.utils import download
from zitkino.models import Cinema, Showtime, ScrapedFilm

from . import scrapers


cinema = Cinema(
    name=u'Kino Art',
    url='http://www.kinoart.cz',
    street=u'Cihlářská 19',
    town=u'Brno',
    coords=(49.2043861, 16.6034708)
)


@scrapers.register(cinema)
class Scraper(object):

    url = 'http://www.tugendhat.eu/cz/aktualne/filmove-projekce.html'

    def __call__(self):
        for entry in self._scrape_index():
            print self._parse_entry(entry)

    def _scrape_index(self):
        resp = download(self.url)
        html = parsers.html(resp.content, base_url=resp.url)
        return html.cssselect('#content div.article-link')

    def _parse_entry(self, entry):
        [news_date] = entry.cssselect('p.news-date')
        date = datetime.datetime.strptime(news_date.text.strip(), '%d.%m.%Y')
        if date < datetime.datetime.now():
            return
        [link] = entry.cssselect('h3 a.page-link')
        url = 'http://www.tugendhat.eu/' + link.attrib['href']
        return entry, url


if __name__ == '__main__':
    print Scraper()()
