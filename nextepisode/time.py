__author__ = 'gabriel'

from datetime import datetime


def str2time(time):
    return datetime.strptime(time, '%b/%d/%Y')


def time2str(time=datetime.now()):
    return time.strftime("%b/%d/%Y")