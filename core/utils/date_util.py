import datetime
import time


class DateUtil(object):

    @staticmethod
    def get_timestamp():
        return int(time.time())

    @staticmethod
    def timestamp_format(timestamp: int, format_str: str = '%Y-%m-%d %H:%M:%S'):
        return datetime.datetime.fromtimestamp(timestamp).strftime(format_str)
