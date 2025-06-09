# -*- coding: utf-8 -*-
#
#  Directory selector
#
#  $Id$
#
#
###################################################
# LOCAL import
###################################################
from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit import TranslateTXT as _
from Plugins.Extensions.IPTVPlayer.components.iptvlist import IPTVMainNavigatorList
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG, printExc, mkdir, IsValidFileName, eConnectCallback
from Plugins.Extensions.IPTVPlayer.components.e2ivkselector import GetVirtualKeyboard

###################################################
from Plugins.Extensions.IPTVPlayer.p2p3.manipulateStrings import ensure_str
###################################################
# FOREIGN import
###################################################
from enigma import eConsoleAppContainer, getDesktop

from Screens.Screen import Screen
from Screens.HelpMenu import HelpableScreen
from Screens.MessageBox import MessageBox
# from Components.Sources.StaticText import StaticText
from Components.Label import Label
from Components.ActionMap import ActionMap
from Tools.BoundFunction import boundFunction
from os import path as os_path
###################################################


class CListItem:
    def __init__(self, name='', fullDir='', type='dir'):
        self.type = type
        self.name = name
        self.fullDir = fullDir

    def getDisplayTitle(self):
        return self.name

    def getTextColor(self):
        return None


class IPTVDirBrowserList(IPTVMainNavigatorList):
    def __init__(self):
        self.ICONS_FILESNAMES = {'dir': 'CategoryItem.png', 'file': 'ArticleItem.png'}
        IPTVMainNavigatorList.__init__(self)


class IPTVDirectorySelectorWidget(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = """
        <screen name="IPTVDirectorySelectorWidget" position="center,center" size="1590,825" title="">
            <widget name="curr_dir" position="12,8" zPosition="2" size="793,45" valign="center" halign="left" font="Regular;28" transparent="1" foregroundColor="white" />
            <widget name="list" position="10,60" zPosition="1" size="800,720" transparent="1" scrollbarMode="showOnDemand" enableWrapAround="1" />

            <eLabel position="0,0" size="820,50" backgroundColor="#000d0f16" zPosition="-1" />
            <eLabel position="0,e-40" size="820,48" backgroundColor="#000d0f16" zPosition="-1" />
            <eLabel position="0,55" size="1590,2" backgroundColor="grey" zPosition="2" />
            <eLabel position="0,e-40" size="1590,2" backgroundColor="grey" zPosition="2" />

            <widget source="session.VideoPicture" render="Pig" position="1032,78" zPosition="1" size="494,272" backgroundColor="transparent" transparent="0" cornerRadius="14" />
            <widget source="Event" render="Label" position="1033,359" size="500,30" font="Regular; 26" transparent="1" halign="right" valign="center" zPosition="99" backgroundColor="background">
                <convert type="EventTime">Remaining</convert>
                <convert type="RemainingToText">InMinutes</convert>
            </widget>

            <!--#####red####/-->
            <ePixmap pixmap="buttons/redbutton.png" position="32,e-40" size="300,6" alphatest="blend" objectTypes="key_red,Button,Label" transparent="1" />
            <widget source="key_red" render="Pixmap" pixmap="buttons/redbutton.png" position="32,e-40" size="300,6" alphatest="blend" objectTypes="key_red,StaticText" transparent="1">
              <convert type="ConditionalShowHide" />
            </widget>
            <widget name="key_red" position="27,e-40" size="310,45" zPosition="11" font="Regular; 30" noWrap="1" valign="center" halign="center" backgroundColor="background" objectTypes="key_red,Button,Label" transparent="1" />
            <widget source="key_red" render="Label" position="27,e-40" size="310,45" zPosition="11" font="Regular; 30" noWrap="1" valign="center" halign="center" backgroundColor="background" objectTypes="key_red,StaticText" transparent="1" />
            <!--#####green####/-->
            <ePixmap pixmap="buttons/greenbutton.png" position="342,e-40" size="300,6" alphatest="blend" objectTypes="key_green,Button,Label" transparent="1" />
            <widget source="key_green" render="Pixmap" pixmap="buttons/greenbutton.png" position="342,e-40" size="300,6" alphatest="blend" objectTypes="key_green,StaticText" transparent="1">
              <convert type="ConditionalShowHide" />
            </widget>
            <widget name="key_green" position="337,e-40" size="310,45" zPosition="11" font="Regular; 30" valign="center" halign="center" backgroundColor="background" objectTypes="key_green,Button,Label" transparent="1" />
            <widget source="key_green" render="Label" position="337,e-40" size="310,45" zPosition="11" font="Regular; 30" valign="center" halign="center" backgroundColor="background" objectTypes="key_green,StaticText" transparent="1" />
            <!--#####yellow####/-->
            <ePixmap pixmap="buttons/yellowbutton.png" position="652,e-40" size="300,6" alphatest="blend" objectTypes="key_yellow,Button,Label" transparent="1" />
            <widget source="key_yellow" render="Pixmap" pixmap="buttons/yellowbutton.png" position="652,e-40" size="300,6" alphatest="blend" objectTypes="key_yellow,StaticText" transparent="1">
              <convert type="ConditionalShowHide" />
            </widget>
            <widget name="key_yellow" position="647,e-40" size="310,45" zPosition="11" font="Regular; 30" noWrap="1" valign="center" halign="center" backgroundColor="background" objectTypes="key_yellow,Button,Label" transparent="1" />
            <widget source="key_yellow" render="Label" position="647,e-40" size="310,45" zPosition="11" font="Regular; 30" noWrap="1" valign="center" halign="center" backgroundColor="background" objectTypes="key_yellow,StaticText" transparent="1" />
            <!--#####blue####/-->
            <ePixmap pixmap="buttons/bluebutton.png" position="962,e-40" size="300,6" alphatest="blend" objectTypes="key_blue,Button,Label" transparent="1" />
            <widget source="key_blue" render="Pixmap" pixmap="buttons/bluebutton.png" position="962,e-40" size="300,6" alphatest="blend" objectTypes="key_blue,StaticText" transparent="1">
              <convert type="ConditionalShowHide" />
            </widget>
            <widget name="key_blue" position="957,e-40" size="310,45" zPosition="11" font="Regular; 30" noWrap="1" valign="center" halign="center" backgroundColor="background" objectTypes="key_blue,Button,Label" transparent="1" />
            <widget source="key_blue" render="Label" position="957,e-40" size="310,45" zPosition="11" font="Regular; 30" noWrap="1" valign="center" halign="center" backgroundColor="background" objectTypes="key_blue,StaticText" transparent="1" />

            <widget source="key_menu" render="Label" position="e-190,e-40" size="55,55" backgroundColor="background" conditional="key_menu" font="Regular; 20" halign="center" valign="center" transparent="1" cornerRadius="26">
                <convert type="ConditionalShowHide" />
            </widget>
            <widget source="key_help" render="Label" position="e-90,e-40" size="55,55" backgroundColor="background" conditional="key_help" font="Regular; 20" halign="center" valign="center" transparent="1" cornerRadius="26">
                <convert type="ConditionalShowHide" />
            </widget>

        </screen>"""

    else:
        skin = """
            <screen name="IPTVDirectorySelectorWidget" position="650,320" size="950,650" title="">
            <widget name="curr_dir" position="10,5" zPosition="2" size="700,45" valign="center" halign="left" font="Regular;18" transparent="1" foregroundColor="white" />
            <widget name="list" position="13,68" zPosition="1" size="580,511" transparent="1" scrollbarMode="showOnDemand" enableWrapAround="1" />

            <!--
            <widget name="key_red" position="46,400" zPosition="2" size="150,35" valign="center" halign="left" font="Regular;22" transparent="1" foregroundColor="red" />
            <widget name="key_green" position="239,400" zPosition="2" size="150,35" valign="center" halign="left" font="Regular;22" transparent="1" foregroundColor="green" />
            <widget name="key_blue" position="444,400" zPosition="2" size="150,35" valign="center" halign="left" font="Regular;22" transparent="1" foregroundColor="blue" />
            <ePixmap position="13,400" zPosition="4" size="30,30" pixmap="%s" transparent="1" alphatest="blend" />
            <ePixmap position="207,400" zPosition="4" size="30,30" pixmap="%s" transparent="1" alphatest="blend" />
            <ePixmap position="404,400" zPosition="4" size="35,30" pixmap="%s" transparent="1" alphatest="blend" />
             -->
            <eLabel position="0,0" size="950,50" backgroundColor="#000d0f16" zPosition="-1" />
            <eLabel position="0,605" size="950,48" backgroundColor="#000d0f16" zPosition="-1" />
            <eLabel position="0,55" size="950,2" backgroundColor="grey" zPosition="2" />
            <eLabel position="0,815" size="950,2" backgroundColor="grey" zPosition="2" />

            <widget source="key_red" render="Label" position="0,e-40" size="180,40" backgroundColor="key_red" font="Regular;20" foregroundColor="key_text" halign="center" valign="center">
                <convert type="ConditionalShowHide" />
            </widget>
            <widget source="key_green" render="Label" position="190,e-40" size="180,40" backgroundColor="key_green" font="Regular;20" foregroundColor="key_text" halign="center" valign="center">
                <convert type="ConditionalShowHide" />
            </widget>
            <widget source="key_yellow" render="Label" position="380,e-40" size="180,40" backgroundColor="key_yellow" conditional="key_yellow" font="Regular;20" foregroundColor="key_text" halign="center" valign="center">
                <convert type="ConditionalShowHide" />
            </widget>
            <widget source="key_blue" render="Label" position="570,e-40" size="180,40" backgroundColor="key_blue" conditional="key_blue" font="Regular;20" foregroundColor="key_text" halign="center" valign="center">
                <convert type="ConditionalShowHide" />
            </widget>
            <widget source="key_menu" render="Label" position="e-190,e-40" size="90,40" backgroundColor="key_back" conditional="key_menu" font="Regular;20" foregroundColor="key_text" halign="center" valign="center">
                <convert type="ConditionalShowHide" />
            </widget>
            <widget source="key_help" render="Label" position="e-90,e-40" size="90,40" backgroundColor="key_back" conditional="key_help" font="Regular;20" foregroundColor="key_text" halign="center" valign="center">
                <convert type="ConditionalShowHide" />
            </widget>

        </screen>"""

    def __init__(self, session, currDir, title="Directory browser"):
        printDBG("IPTVDirectorySelectorWidget.__init__ -------------------------------")
        Screen.__init__(self, session)

        if type(self) is IPTVDirectorySelectorWidget:
            self["key_red"] = Label(_("Cancel"))
            self["key_yellow"] = Label(_("Refresh"))
            self["key_blue"] = Label(_("New dir"))
            self["key_green"] = Label(_("Apply"))
            self["curr_dir"] = Label(_(" "))
            self["list"] = IPTVDirBrowserList()
            self["FilelistActions"] = ActionMap(
                ["ColorActions", "OkCancelActions"],
                {
                    "red": self.requestCancel,
                    "green": self.requestApply,
                    "yellow": self.requestRefresh,
                    "blue": self.requestNewDir,
                    "ok": self.requestOk,
                    "cancel": self.requestBack
                }
            )

        self.title = title
        self.onLayoutFinish.append(self.layoutFinished)
        self.onClose.append(self.__onClose)

        self.console = eConsoleAppContainer()
        self.console_appClosed_conn = eConnectCallback(self.console.appClosed, self.refreshFinished)
        self.console_stderrAvail_conn = eConnectCallback(self.console.stderrAvail, self.refreshNewData)
        self.underRefreshing = False
        self.underClosing = False
        self.deferredAction = None

        try:
            while not os_path.isdir(currDir):
                tmp = os_path.dirname(currDir)
                if tmp == currDir:
                    break
                currDir = tmp
        except Exception:
            currDir = ''
            printExc()

        self.currDir = currDir
        self.currList = []

        self.tmpData = ''
        self.tmpList = []

    def __del__(self):
        printDBG("IPTVDirectorySelectorWidget.__del__ -------------------------------")

    def __onClose(self):
        printDBG("IPTVDirectorySelectorWidget.__onClose -----------------------------")
        if None is not self.console:
            self.console_appClosed_conn = None
            self.console_stderrAvail_conn = None
            self.console_stdoutAvail_conn = None
            self.console.sendCtrlC()
            self.console = None

        self.onClose.remove(self.__onClose)
        self.onLayoutFinish.remove(self.layoutFinished)

    def _iptvDoClose(self, ret=None):
        if self.console:
            self.console.sendCtrlC()
        self.close(ret)

    def _getSelItem(self):
        currSelIndex = self["list"].getCurrentIndex()
        if len(self.currList) <= currSelIndex:
            return None
        return self.currList[currSelIndex]

    def prepareCmd(self):
        cmd = '%s "%s" dl d' % ("/usr/bin/lsdir", self.currDir)
        return cmd

    def doAction(self, action):
        if not self.underRefreshing:
            action()
        else:
            self.deferredAction = action
            self.console.sendCtrlC()

    def layoutFinished(self):
        printDBG("IPTVDirectorySelectorWidget.layoutFinished -------------------------------")
        self.setTitle(_(self.title))
        self.currDirChanged()

    def currDirChanged(self):
        printDBG("IPTVDirectorySelectorWidget.currDirChanged")
        self.currDir = self.getCurrentDirectory()
        self["curr_dir"].setText(_(self.currDir))
        self["list"].setList([])
        self.requestRefresh()

    def getCurrentDirectory(self):
        if self.currDir and os_path.isdir(self.currDir):
            if '/' != self.currDir[-1]:
                self.currDir += '/'
            return self.currDir
        else:
            return "/"

    def refreshFinished(self, code):
        printDBG("IPTVDirectorySelectorWidget.refreshFinished")
        self.underRefreshing = False
        if None is not self.deferredAction:
            deferredAction = self.deferredAction
            self.deferredAction = None
            deferredAction()
        else:
            printDBG("IPTVDirectorySelectorWidget.refreshFinished fill list")
            # sort list and set
            self.currList = []
            self.tmpList.sort(key=lambda x: x.name.lower())
            self.currList = self.tmpList
            if ('/' != self.currDir):
                self.currList.insert(0, CListItem(name='..', fullDir='', type='dir'))  # add back item
            self["list"].setList([(x,) for x in self.currList])
            self.tmpList = []
            self.tmpData = ''

    def refreshNewData(self, data):
        self.tmpData += ensure_str(data)
        newItems = self.tmpData.split('\n')
        if self.tmpData.endswith('\n'):
            self.tmpData = ''
        else:
            self.tmpData = newItems[-1]
            del newItems[-1]
        self.doRefreshNewData(newItems)

    def doRefreshNewData(self, newItems):
        for item in newItems:
            params = item.split('//')
            if item.startswith('.'):
                continue  # do not list hidden items
            # printDBG(params)
            if 4 == len(params):
                # if '0' == params[2]: type = 'dir'
                # else: type = 'linkdir'
                self.tmpList.append(CListItem(name=params[0], fullDir=params[3], type='dir'))

    def requestApply(self):
        if self.underClosing:
            return
        self.doAction(boundFunction(self._iptvDoClose, self.getCurrentDirectory()))

    def requestCancel(self):
        printDBG(">>>REQUEST CANCEL<<<")
        try:
            running = self.console.running()
        except Exception:
            running = True
        if not self.console or not running:
            self._iptvDoClose(None)
        else:
            self.doAction(boundFunction(self._iptvDoClose, None))

    def requestRefresh(self):
        if self.underClosing:
            return
        if self.underRefreshing:
            return
        self.underRefreshing = True
        self.tmpList = []
        self.tmpData = ''
        cmd = self.prepareCmd()
        printDBG("IPTVDirectorySelectorWidget.requestRefresh cmd[%s]" % cmd)
        # self.console.setNice(GetNice() + 2)
        # self.console.execute(cmd)
        self.console.execute("nice -n 2 %s" % cmd)

    def requestNewDir(self):
        if self.underClosing:
            return
        self.doAction(self.newDir)

    def requestOk(self):
        if self.underClosing:
            return
        self.doAction(self.ok)

    def requestBack(self):
        if self.underClosing:
            return
        self.doAction(self.back)

    def ok(self):
        item = self._getSelItem()
        if None is item or '' == item.name:
            return
        fullDirName = os_path.join(self.currDir, item.name)
        if '..' == item.name:
            return self.back()
        if os_path.isdir(fullDirName):
            self.currDir = fullDirName
            self.currDirChanged()

    def back(self):
        if '/' == self.currDir:
            self._iptvDoClose(None)
        else:
            self.currDir = self.currDir[:self.currDir[:-1].rfind('/')]
            self.currDirChanged()

    def newDir(self):
        self.session.openWithCallback(self.enterPatternCallBack, GetVirtualKeyboard(), title=(_("Enter name")), text="")

    def enterPatternCallBack(self, newDirName=None):
        if None is not self.currDir and newDirName is not None:
            sts = False
            if IsValidFileName(newDirName):
                try:
                    sts, msg = mkdir(os_path.join(self.currDir, newDirName))
                except Exception:
                    sts, msg = False, _("Exception occurs")
            else:
                msg = _("Invalid name.")
            if sts:
                self.requestRefresh()
            else:
                self.session.open(MessageBox, msg, type=MessageBox.TYPE_INFO, timeout=5)


class IPTVFileSelectorWidget(IPTVDirectorySelectorWidget):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = """
        <screen name="IPTVFileSelectorWidget" position="center,center" size="820,860" title="">
            <!-- add lululla -->
            <eLabel position="0,0" size="800,45" backgroundColor="#000d0f16" zPosition="-1" />
            <eLabel position="0,e-40" size="800,48" backgroundColor="#000d0f16" zPosition="-1" />
            <eLabel position="0,45" size="800,2" backgroundColor="grey" zPosition="2" />
            <eLabel position="0,e-40" size="800,2" backgroundColor="grey" zPosition="2" />

            <!--#####red####/-->
            <ePixmap pixmap="buttons/redbutton.png" position="32,e-40" size="300,6" alphatest="blend" objectTypes="key_red,Button,Label" transparent="1" />
            <widget source="key_red" render="Pixmap" pixmap="buttons/redbutton.png" position="32,e-40" size="300,6" alphatest="blend" objectTypes="key_red,StaticText" transparent="1">
              <convert type="ConditionalShowHide" />
            </widget>
            <widget name="key_red" position="27,e-40" size="310,45" zPosition="11" font="Regular; 30" noWrap="1" valign="center" halign="center" backgroundColor="background" objectTypes="key_red,Button,Label" transparent="1" />
            <widget source="key_red" render="Label" position="27,e-40" size="310,45" zPosition="11" font="Regular; 30" noWrap="1" valign="center" halign="center" backgroundColor="background" objectTypes="key_red,StaticText" transparent="1" />

            <widget name="curr_dir" position="10,5" zPosition="2" size="750,40" valign="center" halign="left" font="Regular;28" transparent="1" foregroundColor="white" />
            <widget name="list" position="10,50" zPosition="1" size="800,725" transparent="1" scrollbarMode="showOnDemand" enableWrapAround="1" />
        </screen>"""
    else:
        skin = """
        <screen name="IPTVFileSelectorWidget" position="center,center" size="620,440" title="">
            <!-- add lululla -->
            <eLabel position="0,0" size="600,45" backgroundColor="#000d0f16" zPosition="-1" />
            <eLabel position="0,e-40" size="600,48" backgroundColor="#000d0f16" zPosition="-1" />
            <eLabel position="0,45" size="600,2" backgroundColor="grey" zPosition="2" />
            <eLabel position="0,e-40" size="600,2" backgroundColor="grey" zPosition="2" />

            <!--#####red####/-->
            <ePixmap pixmap="buttons/redbutton.png" position="32,e-40" size="200,6" alphatest="blend" objectTypes="key_red,Button,Label" transparent="1" />
            <widget source="key_red" render="Pixmap" pixmap="buttons/redbutton.png" position="32,e-40" size="200,6" alphatest="blend" objectTypes="key_red,StaticText" transparent="1">
              <convert type="ConditionalShowHide" />
            </widget>
            <widget name="key_red" position="27,e-40" size="210,45" zPosition="11" font="Regular; 24" noWrap="1" valign="center" halign="center" backgroundColor="background" objectTypes="key_red,Button,Label" transparent="1" />
            <widget source="key_red" render="Label" position="27,e-40" size="210,45" zPosition="11" font="Regular; 24" noWrap="1" valign="center" halign="center" backgroundColor="background" objectTypes="key_red,StaticText" transparent="1" />

            <widget name="curr_dir" position="10,5" zPosition="2" size="600,35" valign="center" halign="left" font="Regular;18" transparent="1" foregroundColor="white" />
            <widget name="list" position="10,45" zPosition="1" size="580,335" transparent="1" scrollbarMode="showOnDemand" enableWrapAround="1" />
        </screen>"""

    def __init__(self, session, currDir, title="File browser", fileMatch=None):
        printDBG("IPTVFileSelectorWidget.__init__ -------------------------------")
        IPTVDirectorySelectorWidget.__init__(self, session, currDir, title)

        if type(self) is IPTVFileSelectorWidget:
            self["key_red"] = Label(_("Cancel"))
            self["curr_dir"] = Label(_(" "))
            self["list"] = IPTVDirBrowserList()
            self["FilelistActions"] = ActionMap(
                ["ColorActions", "SetupActions"],
                {
                    "red": self.close,
                    "ok": self.requestOk,
                    "cancel": self.close
                    # "yellow": self.requestRefresh
                }
            )

        self.fileMatch = fileMatch

    def prepareCmd(self):
        cmd = '%s "%s" drl dr' % ("/usr/bin/lsdir", self.currDir)
        return cmd

    def doRefreshNewData(self, newItems):
        for item in newItems:
            params = item.split('//')
            if item.startswith('.'):
                continue  # do not list hidden items
            # printDBG(params)
            if 4 == len(params):
                if 'd' == params[1]:
                    type = 'dir'
                else:
                    type = 'file'
                    try:
                        if None is not self.fileMatch and None is self.fileMatch.match(params[0]):
                            continue
                    except Exception:
                        printExc()
                        continue
                self.tmpList.append(CListItem(name=params[0], fullDir=params[3], type=type))

    def requestOk(self):
        item = self._getSelItem()
        if None is item or '' == item.name:
            return
        fullPath = os_path.join(self.currDir, item.name)
        if item.type == 'dir':
            if '..' == item.name:
                return self.back()
            if os_path.isdir(fullPath):
                self.currDir = fullPath
                self.currDirChanged()
        elif item.type == 'file':
            self.requestApply(fullPath)

    def requestApply(self, fullPath):
        if self.underClosing:
            return
        self.doAction(boundFunction(self._iptvDoClose, fullPath))
