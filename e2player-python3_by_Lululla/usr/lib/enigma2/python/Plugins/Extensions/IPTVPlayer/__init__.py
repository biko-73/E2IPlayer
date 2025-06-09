# -*- coding: utf-8 -*-

from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from Components.SystemInfo import BoxInfo
from Components.config import config, ConfigSubsection
import gettext

GRIDSUPPORT = BoxInfo.getItem("distro") in ("openatv", )


PluginLanguageDomain = "IPTVPlayer"
PluginLanguagePath = "Extensions/IPTVPlayer/locale"


def localeInit():
	gettext.bindtextdomain(PluginLanguageDomain, resolveFilename(SCOPE_PLUGINS, PluginLanguagePath))


def _(txt):
	t = gettext.dgettext(PluginLanguageDomain, txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t


localeInit()
language.addCallback(localeInit)


# Inizializza la configurazione principale se non esiste
if not hasattr(config.plugins, 'iptvplayer'):
	config.plugins.iptvplayer = ConfigSubsection()
