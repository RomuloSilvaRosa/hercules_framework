from datetime import datetime


class ExpirationTime:
    minute = 60
    hour = minute * 60
    day = 24 * hour


def datenow():
    return datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

