class Addon(object):
    def __init__(self, id=None):
        pass

    def getLocalizedString(self, id):
        return unicode

    def getSetting(self, id):
        return unicode

    def setSetting(self, id, value):
        pass

    def openSettings(self):
        pass

    def getAddonInfo(self, id):
        return str
