__author__ = "Gabriel Melillo<gabriel@melillo.me>"
__version__ = "0.5"

import mechanize
from uuid import uuid3, NAMESPACE_OID
from urllib import urlencode
from re import search as reg_search
from httplib2 import Http
from bs4 import BeautifulSoup
from datetime import datetime


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
        self.today_list = []

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
                try:
                    self._add_value({
                        'Name': [link.contents[0]],
                        'index': uuid3(NAMESPACE_OID, link.get('href').encode('utf8', 'ignore')).__str__(),
                        'URL': link.get('href').encode('utf8', 'ignore')
                    })
                except UnicodeDecodeError:
                    self._add_value({
                        'Name': [link.contents[0]],
                        'index': 'N/A',
                        'URL': link.get('href').encode('utf8', 'ignore')
                    })

    @staticmethod
    def do_regexp(regexp, data, number=1, default='N/A'):
        m = reg_search(regexp, data)
        if m is not None:
            return m.group(number)
        else:
            return default

    def attach_tvrage_info(self):
        for idx, show in enumerate(self.list):
            h = Http('.cache')
            url = "http://services.tvrage.com/tools/quickinfo.php?{}".format(
                urlencode({
                    'show': show['Name'][0].__str__(),
                    'exact': 1
                })
            )

            resp, content = h.request(url)

            self.list[idx]['TV Rage'] = {
                'Show ID': self.do_regexp("Show ID@([0-9]{0,5})\\n", content),
                'Show Name': self.do_regexp("Show Name@([a-zA-Z0-9_'\. ]*)\\n", content),
                'URL': self.do_regexp("Show URL@([a-zA-Z0-9_'\. /:-]*)\\n", content),
                'Premiered': self.do_regexp('Premiered@([0-9]{4})\\n', content),
                'Country': self.do_regexp('Country@([a-zA-Z]*)\\n', content),
                'Status': self.do_regexp('Status@([a-zA-Z /]*)\\n', content),
                'Classification': self.do_regexp('Classification@([a-zA-Z -]*)\\n', content),
                'Genres': self.do_regexp('Genres@([a-zA-Z |/\-]*)\\n', content),
                'Network': self.do_regexp('Network@([a-zA-Z |\(\)]*)\\n', content),
            }
            latest_episode = reg_search('Latest Episode@([0-9x]*)\^(.*)\^([a-zA-Z0-9/]*)\\n', content)
            if latest_episode is not None:
                self.list[idx]['TV Rage']['Latest Episode'] = {
                    'Number': latest_episode.group(1),
                    'Title': latest_episode.group(2),
                    'Air Date': latest_episode.group(3)
                }
            else:
                self.list[idx]['TV Rage']['Latest Episode'] = {
                    'Number': 'N/A',
                    'Title': 'N/A',
                    'Air Date': 'N/A'
                }
            next_episode = reg_search('Next Episode@([0-9x]*)\^(.*)\^([a-zA-Z0-9/]*)\\n', content)
            if next_episode is not None:
                self.list[idx]['TV Rage']['Next Episode'] = {
                    'Number': next_episode.group(1),
                    'Title': next_episode.group(2),
                    'Air Date': next_episode.group(3)
                }
            else:
                self.list[idx]['TV Rage']['Next Episode'] = {
                    'Number': 'N/A',
                    'Title': 'N/A',
                    'Air Date': 'N/A'
                }
            if reg_search('Airtime@([a-zA-Z0-9 :]*)\\n', content) is not None:
                self.list[idx]['TV Rage']['Airtime'] = reg_search('Airtime@([a-zA-Z0-9 :]*)\\n', content).group(1)
            else:
                self.list[idx]['TV Rage']['Airtime'] = 'N/A'

            if datetime.now().strftime("%b/%d/%Y") == self.list[idx]['TV Rage']['Next Episode']['Air Date']:
                self.today_list.append(self.list[idx])
            if datetime.now().strftime("%b/%d/%Y") == self.list[idx]['TV Rage']['Latest Episode']['Air Date']:
                self.today_list.append(self.list[idx])