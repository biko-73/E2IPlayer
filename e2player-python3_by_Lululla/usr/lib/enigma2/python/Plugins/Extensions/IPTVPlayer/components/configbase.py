# -*- coding: utf-8 -*-
#
#  Konfigurator dla iptv 2013
#  autorzy: j00zek, samsamsam
#


###################################################
# LOCAL import
###################################################
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG, printExc, GetIPTVPlayerVersion  # , GetIconDir
from Plugins.Extensions.IPTVPlayer.components.iptvdirbrowser import IPTVDirectorySelectorWidget, IPTVFileSelectorWidget
from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit import TranslateTXT as _
from Plugins.Extensions.IPTVPlayer.components.e2ivkselector import GetVirtualKeyboard
###################################################

###################################################
# FOREIGN import
###################################################
import re

from Screens.MessageBox import MessageBox
from Screens.Screen import Screen

from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.config import ConfigDirectory, ConfigText, ConfigPassword, ConfigBoolean, ConfigSelection, configfile
from Components.ConfigList import ConfigListScreen
from Components.Sources.StaticText import StaticText
from Tools.BoundFunction import boundFunction
###################################################
COLORS_DEFINITONS = [("#000000", _("black")), ("#C0C0C0", _("silver")), ("#808080", _("gray")), ("#FFFFFF", _("white")), ("#800000", _("maroon")), ("#FF0000", _("red")), ("#800080", _("purple")), ("#FF00FF", _("fuchsia")),
                     ("#008000", _("green")), ("#00FF00", _("lime")), ("#808000", _("olive")), ("#FFFF00", _("yellow")), ("#000080", _("navy")), ("#0000FF", _("blue")), ("#008080", _("teal")), ("#00FFFF", _("aqua"))]


class ConfigIPTVFileSelection(ConfigDirectory):
    def __init__(self, ignoreCase=True, fileMatch=None, default="", visible_width=60):
        self.fileMatch = fileMatch
        self.ignoreCase = ignoreCase
        ConfigDirectory.__init__(self, default, visible_width)


class ConfigBaseWidget(Screen, ConfigListScreen):
    skin = """
            <screen position="center,center" size="1590,825" title="E2iPlayer Config %s">
                <widget name="config" position="30,69" size="926,670" zPosition="1" transparent="1" scrollbarMode="showOnDemand" enableWrapAround="1" font="Regular;22" itemHeight="32" />

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

                <widget name="footnote" position="30,9" zPosition="2" size="920,52" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="white" />
                <widget source="session.VideoPicture" render="Pig" position="1032,78" zPosition="1" size="494,272" backgroundColor="transparent" transparent="0" cornerRadius="14" />

                <widget source="Event" render="Label" position="1033,359" size="500,30" font="Regular; 26" transparent="1" halign="right" valign="center" zPosition="99" backgroundColor="background">
                    <convert type="EventTime">Remaining</convert>
                    <convert type="RemainingToText">InMinutes</convert>
                </widget>
            </screen>""" % (GetIPTVPlayerVersion())  # , GetIconDir('red.png'), GetIconDir('green.png'), GetIconDir('yellow.png'), GetIconDir('blue.png'))

    def __init__(self, session):
        printDBG("ConfigBaseWidget.__init__ -------------------------------")

        Screen.__init__(self, session)

        self.skinName = ["ConfigBaseWidget"]

        self.onChangedEntry = []
        self.list = []
        ConfigListScreen.__init__(self, self.list, session=session, on_change=self.changedEntry)
        self.setup_title = (_("E2iPlayer - settings"))

        self["key_green"] = StaticText(_("Save"))
        self["footnote"] = Label(_(" "))
        self["key_red"] = StaticText(_("Cancel"))

        self["key_blue"] = StaticText()
        self["key_yellow"] = StaticText()

        self["actions"] = ActionMap(
            ["IPTVPlayerListActions"],
            {
                "menu": self.keyMenu,
            },
            -2
        )

        self["actions"] = ActionMap(
            ["SetupActions", "ColorActions", "WizardActions", "ListboxActions"],
            {
                "cancel": self.keyExit,
                "green": self.keySave,
                "ok": self.keyOK,
                "red": self.keyCancel,
                "yellow": self.keyYellow,
                "blue": self.keyBlue,

                "up": self.keyUp,
                "down": self.keyDown,
                "moveUp": self.keyUp,
                "moveDown": self.keyDown,
                "moveTop": self.keyHome,
                "moveEnd": self.keyEnd,
                "home": self.keyHome,
                "end": self.keyEnd,
                "pageUp": self.keyPageUp,
                "pageDown": self.keyPageDown
            },
            -2
        )

        self.onLayoutFinish.append(self.layoutFinished)
        self.onClose.append(self.__onClose)
        self.isOkEnabled = False
        self.hiddenOptionsSecretCode = ""

    def __del__(self):
        printDBG("ConfigBaseWidget.__del__ -------------------------------")

    def __onClose(self):
        printDBG("ConfigBaseWidget.__onClose -----------------------------")
        self.onClose.remove(self.__onClose)
        self.onLayoutFinish.remove(self.layoutFinished)
        if self.onSelectionChanged in self["config"].onSelectionChanged:
            self["config"].onSelectionChanged.remove(self.onSelectionChanged)

    def layoutFinished(self):
        self.setTitle(_("E2iPlayer - settings"))
        if self.onSelectionChanged not in self["config"].onSelectionChanged:
            self["config"].onSelectionChanged.append(self.onSelectionChanged)
        self.runSetup()

    def onSelectionChanged(self):
        self.isOkEnabled = self.isOkActive()
        self.isSelectable = self.isSelectableActive()
        self.setOKLabel()

    def isHiddenOptionsUnlocked(self):
        if "ybybyybb" == self.hiddenOptionsSecretCode:
            return True
        else:
            return False

    def setOKLabel(self):
        if self.isSelectable:
            labelText = "<  %s  >"
        else:
            labelText = "   %s   "
        if self.isOkEnabled:
            labelText = labelText % "OK"
        else:
            labelText = labelText % "  "
        self["footnote"].setText(_(labelText))

    def isOkActive(self):
        if self["config"].getCurrent() is not None:
            currItem = self["config"].getCurrent()[1]
            if isinstance(currItem, ConfigText) or isinstance(currItem, ConfigPassword):
                try:
                    # I really do not like this "help screen" NumericalTextInputHelpDialog which cover others options
                    # it is much easier to type text with VK after OK press, but maybe option need to be added to allow user to have this "help"
                    currItem.help_window.hide()
                except Exception:
                    pass
                return True
        return False

    def isSelectableActive(self):
        if self["config"].getCurrent() is not None:
            currItem = self["config"].getCurrent()[1]
            if currItem and isinstance(currItem, ConfigSelection) or isinstance(currItem, ConfigBoolean):
                return True
        return False

    def runSetup(self):
        self["config"].list = self.list
        self["config"].setList(self.list)

    def isChanged(self):
        bChanged = False
        for x in self["config"].list:
            if x[1].isChanged():
                bChanged = True
                break
        printDBG("ConfigMenu.isChanged bChanged[%r]" % bChanged)
        return bChanged

    def getMessageAfterSave(self):
        return ''

    def getMessageBeforeClose(self):
        return ''

    def askForSave(self, callbackYesFun, callBackNoFun):
        self.session.openWithCallback(boundFunction(self.saveOrCancelChanges, callbackYesFun, callBackNoFun), MessageBox, text=_('Save changes?'), type=MessageBox.TYPE_YESNO)
        return

    def saveOrCancelChanges(self, callbackFun=None, failCallBackFun=None, answer=None):
        if answer:
            self.save()
            if callbackFun:
                callbackFun()
        else:
            self.cancel()
            if failCallBackFun:
                failCallBackFun()

    def keySave(self):
        self.saveAndClose()

    def saveOrCancel(self, operation="save"):
        for x in self["config"].list:
            if "save" == operation:
                x[1].save()
            else:
                x[1].cancel()
        if "save" == operation:
            configfile.save()

    def save(self):
        self.saveOrCancel("save")

    def cancel(self):
        self.saveOrCancel("cancel")
        self.runSetup()

    def saveAndClose(self):
        self.save()
        self.performCloseWithMessage(True)

    def performCloseWithMessage(self, afterSave=True):
        if afterSave:
            message = self.getMessageAfterSave()
        else:
            message = self.getMessageBeforeClose()
        if message == '':
            self.close()
        else:
            self.session.openWithCallback(self.closeAfterMessage, MessageBox, text=message, type=MessageBox.TYPE_INFO)

    def closeAfterMessage(self, arg=None):
        self.close()

    def cancelAndClose(self):
        self.cancel()
        self.performCloseWithMessage()

    def keyOK(self):
        if not self.isOkEnabled:
            return

        curIndex = self["config"].getCurrentIndex()
        currItem = self["config"].list[curIndex][1]

        if isinstance(currItem, ConfigIPTVFileSelection):
            def SetFilePathCallBack(curIndex, newPath):
                if None is not newPath:
                    self["config"].list[curIndex][1].value = newPath
            try:
                if None is not currItem.fileMatch:
                    if currItem.ignoreCase:
                        fileMatch = re.compile(currItem.fileMatch, re.IGNORECASE)
                    else:
                        fileMatch = re.compile(currItem.fileMatch)
                else:
                    fileMatch = None
            except Exception:
                printExc()
                return
            self.session.openWithCallback(boundFunction(SetFilePathCallBack, curIndex), IPTVFileSelectorWidget, currItem.value, _('Select the file'), fileMatch)
            return

        elif isinstance(currItem, ConfigDirectory):
            def SetDirPathCallBack(curIndex, newPath):
                if None is not newPath:
                    self["config"].list[curIndex][1].value = newPath
            self.session.openWithCallback(boundFunction(SetDirPathCallBack, curIndex), IPTVDirectorySelectorWidget, currDir=currItem.value, title=_('Select the directory'))
            return
        elif isinstance(currItem, ConfigText):
            def VirtualKeyBoardCallBack(curIndex, newTxt):
                if isinstance(newTxt, str):
                    self["config"].list[curIndex][1].value = newTxt
            try:
                # we need hide NumericalTextInputHelpDialog before
                self["config"].list[curIndex][1].help_window.hide()
            except Exception:
                printExc()
            self.session.openWithCallback(boundFunction(VirtualKeyBoardCallBack, curIndex), GetVirtualKeyboard(), title=(_("Enter a value")), text=currItem.value)
            return

        ConfigListScreen.keyOK(self)

    def keyExit(self):
        if self.isChanged():
            self.askForSave(self.saveAndClose, self.cancelAndClose)
        else:
            self.performCloseWithMessage()

    def keyCancel(self):
        self.cancelAndClose()

    def keyYellow(self):
        self.hiddenOptionsSecretCode += "y"
        self.runSetup()
        self.keyPageUp()

    def keyBlue(self):
        self.hiddenOptionsSecretCode += "b"
        self.runSetup()
        self.keyPageDown()

    def keyMenu(self):  # hide/unhide hidden options
        if self.hiddenOptionsSecretCode == "ybybyybb":
            self.hiddenOptionsSecretCode = ""
        else:
            self.hiddenOptionsSecretCode = "ybybyybb"
        self.runSetup()

    def keyUp(self):
        if self["config"].instance is not None:
            self["config"].instance.moveSelection(self["config"].instance.moveUp)

    def keyDown(self):
        if self["config"].instance is not None:
            self["config"].instance.moveSelection(self["config"].instance.moveDown)

    def keyPageUp(self):
        if self["config"].instance is not None:
            self["config"].instance.moveSelection(self["config"].instance.pageUp)

    def keyPageDown(self):
        if self["config"].instance is not None:
            self["config"].instance.moveSelection(self["config"].instance.pageDown)

    def keyHome(self):
        pass

    def keyEnd(self):
        pass

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)

    def keyRight(self):
        ConfigListScreen.keyRight(self)

    def getSubOptionsList(self):
        tab = []
        return tab

    def changeSubOptions(self):
        if self["config"].getCurrent()[1] in self.getSubOptionsList():
            self.runSetup()

    def changedEntry(self):
        self.changeSubOptions()
        for x in self.onChangedEntry:
            x()
