__author__ = "Gabriel Melillo<gabriel@melillo.me>"
__version__ = "0.5"

import mechanize
from uuid import uuid3, NAMESPACE_URL
from bs4 import BeautifulSoup


class List(object):
    list = []

    def __init__(self, defaultlist=[]):
        self.list = defaultlist

    def __getitem__(self, item):
        return self.list[item]

    def __iter__(self):
        for item in self.list:
            yield item

    def __len__(self):
        return len(self.list)

    def __setitem__(self, key, value):
        self.list[key] = value

    def __repr__(self):
        return repr(self.list)

    def __str__(self):
        return self.__repr__()

    def _add_value(self, value):
        for item in self.list:
            if item == value:
                return False
        self.list.append(value)
        return True


class NextEpisode(List):
    def __init__(self, username, password, autologin=True, autoupdate=True):
        super(List, self).__init__()
        self.browser = mechanize.Browser()
        self.add_show = self._add_value

        if autologin:
            self.do_login(
                username=username,
                password=password
            )

        if autoupdate:
            self.update_list()

    def do_login(self, username, password):
        self.browser.open("http://next-episode.net/")
        self.browser.select_form(name="login")
        self.browser.form['username'] = username
        self.browser.form['password'] = password
        self.browser.submit()

    def update_list(self):
        html = self.browser.open('http://next-episode.net/settings?action=manageWL').read()
        soup = BeautifulSoup(html)
        divs = soup.findAll('div',
                            attrs={
                                'class': 'leftColumn'
                            })
        self.list = []
        for div in divs:
            links = div.findAll('a', attrs={'class': 'name'})
            for link in links:
                if link.contents[0] == "V":
                    link.contents[0] = "V (2009)"
                self._add_value({
                    'Name': [link.contents[0]],
                    'index': uuid3(NAMESPACE_URL, link.get('href')).__str__(),
                    'URL': link.get('href')
                })