import re


class String:

    @staticmethod
    def addslashed(text):
        tmp = re.sub(re.compile('<.*?>'), '', text)
        tmp = tmp.replace('"', '\\"')
        tmp = tmp.replace("'", "\\'")
        return tmp
