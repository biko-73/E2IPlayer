# -*- coding: utf-8 -*-
#
#  Player Selector
#
#  $Id$
#  Page Punkte weiter ausseinander - 132
#  Version dazu gebaut , skin 14 , 227-229
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from enigma import ePoint, getDesktop
from Tools.LoadPixmap import LoadPixmap
from Components.Label import Label
from Components.config import config
from Screens.ChoiceBox import ChoiceBox
from Components.Sources.StaticText import StaticText

from Plugins.Extensions.IPTVPlayer.components.cover import Cover3
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG, printExc, GetIPTVPlayerVersion, GetIconDir, GetAvailableIconSize
from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit import TranslateTXT as _


class PlayerSelectorWidget(Screen):
    LAST_SELECTION = {}

    def __init__(self, session, inList, outList, numOfLockedItems=0, groupName='', groupObj=None):
        printDBG("PlayerSelectorWidget.__init__ --------------------------------")

        iconSize = GetAvailableIconSize()
        screenwidth = getDesktop(0).size().width()
        # screenheight = getDesktop(0).size().height()

        # ======================================================================
        # MODIFICA PRINCIPALE: Calcolo dinamico di righe e colonne
        # ======================================================================
        max_cols = 5
        max_rows = 4
        try:
            confNumOfRow = int(config.plugins.iptvplayer.numOfRow.value)
            confNumOfCol = int(config.plugins.iptvplayer.numOfCol.value)
            # 0 - means AUTO
            if confNumOfRow > 0:
                max_rows = confNumOfRow
            if confNumOfCol > 0:
                max_cols = confNumOfCol
        except Exception:
            pass

        # Dimensioni base per HD (1280x720)
        if screenwidth <= 1280:
            # Per schermi HD, massimo 5 colonne e 4 righe
            # max_cols = 5
            # max_rows = 4

            # Calcolo effettivo basato sul numero di elementi
            if len(inList) > max_cols * max_rows:
                numOfCol = max_cols
                numOfRow = max_rows
            elif len(inList) > (max_cols - 1) * max_rows:
                numOfCol = max_cols
                numOfRow = min(max_rows, (len(inList) + max_cols - 1) // max_cols)
            else:
                numOfCol = min(max_cols, max(3, len(inList)))
                numOfRow = min(max_rows, (len(inList) + numOfCol - 1) // numOfCol)

        # Per risoluzioni superiori (FHD)
        else:
            # Calcola il numero massimo di colonne in base alla larghezza dello schermo
            max_cols = max(3, min(8, screenwidth // (iconSize + 20)))

            # Calcola il numero massimo di righe in base all'altezza disponibile
            available_height = 740 - 100  # 740 è la posizione Y della barra inferiore, 100 è l'offset superiore
            max_rows = max(2, min(3, available_height // (iconSize + 20)))

            # Calcola il numero effettivo di colonne in base al numero di elementi
            if len(inList) > max_cols * max_rows:
                numOfCol = max_cols
                numOfRow = max_rows
            elif len(inList) > (max_cols - 1) * max_rows:
                numOfCol = max_cols
                numOfRow = min(max_rows, (len(inList) + max_cols - 1) // max_cols)
            else:
                numOfCol = min(max_cols, max(3, len(inList)))
                numOfRow = min(max_rows, (len(inList) + numOfCol - 1) // numOfCol)

        offsetCoverX = 25
        if screenwidth and screenwidth > 1280:
            offsetCoverY = 100
        else:
            offsetCoverY = 80

        # ======================================================================
        # FINE MODIFICA
        # ======================================================================

        # image size
        coverWidth = iconSize
        coverHeight = iconSize

        # space/distance between images
        disWidth = int(coverWidth / 3)
        disHeight = int(coverHeight / 4)

        # marker size should be larger than img
        markerWidth = 45 + coverWidth
        markerHeight = 45 + coverHeight

        # position of first marker
        offsetMarkerX = int(offsetCoverX - (markerWidth - coverWidth) / 2)
        offsetMarkerY = int(offsetCoverY - (markerHeight - coverHeight) / 2)

        self.numOfRow = numOfRow
        self.numOfCol = numOfCol

        tmpX = coverWidth + disWidth
        tmpY = coverHeight + disHeight

        # position of first cover
        self.offsetCoverX = offsetCoverX
        self.offsetCoverY = offsetCoverY
        # space/distance between images
        self.disWidth = disWidth
        self.disHeight = disHeight
        # image size
        self.coverWidth = coverWidth
        self.coverHeight = coverHeight
        # marker size should be larger than img
        self.markerWidth = markerWidth
        self.markerHeight = markerHeight

        self.inList = list(inList)
        self.currList = self.inList
        self.outList = outList

        self.groupName = groupName
        self.groupObj = groupObj
        self.numOfLockedItems = numOfLockedItems

        self.IconsSize = iconSize  # do ladowania ikon
        self.MarkerSize = self.IconsSize + 45

        self.lastSelection = PlayerSelectorWidget.LAST_SELECTION.get(self.groupName, 0)
        self.calcDisplayVariables()

        # pagination
        self.pageItemSize = 16
        self.pageItemStartX = int((offsetCoverX + tmpX * numOfCol + offsetCoverX - disWidth - self.numOfPages * self.pageItemSize) / 2)
        if screenwidth and screenwidth == 1280:
            self.pageItemStartY = 60
        else:
            self.pageItemStartY = 40

        if screenwidth and screenwidth > 1280:
            # wenn einer die version einbauen will <widget name="IptvVersion" position="40,0" zPosition="1" size="250,50" font="Regular;36" halign="center" valign="center" transparent="1"/>
            skin = """
            <screen name="PlayerSelectorWidget" position="center,center" title="E2iPlayer %s" size="1590,825">
                <eLabel position="0,0" size="1590,88" backgroundColor="#000d0f16" zPosition="-1" />
                <eLabel position="0,e-48" size="1590,48" backgroundColor="#000d0f16" zPosition="-1" />
                <eLabel position="0,85" size="1590,2" backgroundColor="grey" zPosition="2" />
                <eLabel position="0,e-45" size="1590,2" backgroundColor="grey" zPosition="2" />

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

                <widget name="statustext" position="0,0" zPosition="1" size="%d,50" font="Regular;36" halign="center" valign="center" transparent="1"/>
                <widget name="marker" zPosition="2" position="%d,%d" size="%d,%d" transparent="1" alphatest="blend" />
                <widget name="page_marker" zPosition="3" position="%d,%d" size="%d,%d" transparent="1" alphatest="blend" />
                <widget name="menu" zPosition="3" position="%d,10" size="70,30" transparent="1" alphatest="blend" />

                """ % (

                GetIPTVPlayerVersion(),
                # GetIconDir('red.png'), GetIconDir('green.png'), GetIconDir('yellow.png'), GetIconDir('blue.png'),
                offsetCoverX + tmpX * numOfCol + offsetCoverX - disWidth,  # width of status line
                offsetMarkerX, offsetMarkerY,  # first marker position
                markerWidth, markerHeight,    # marker size
                self.pageItemStartX, self.pageItemStartY,  # pagination marker
                self.pageItemSize, self.pageItemSize,
                offsetCoverX + tmpX * numOfCol + offsetCoverX - disWidth - 70,
            )
        else:
            skin = """
            <screen name="PlayerSelectorWidget" position="center,center" title="E2iPlayer %s" size="1280,720">
            <eLabel position="0,0" size="1280,88" backgroundColor="#000d0f16" zPosition="-1" />
            <eLabel position="0,e-40" size="1280,48" backgroundColor="#000d0f16" zPosition="-1" />
            <eLabel position="0,85" size="1280,2" backgroundColor="grey" zPosition="2" />
            <eLabel position="0,e-45" size="1280,2" backgroundColor="grey" zPosition="2" />

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
            
            <widget name="statustext" position="0,0" zPosition="1" size="%d,50" font="Regular;26" halign="center" valign="center" transparent="1"/>
            <widget name="marker" zPosition="2" position="%d,%d" size="%d,%d" transparent="1" alphatest="blend" />
            <widget name="page_marker" zPosition="3" position="%d,%d" size="%d,%d" transparent="1" alphatest="blend" />
            <widget name="menu" zPosition="3" position="%d,10" size="70,30" transparent="1" alphatest="blend" />
            """ % (
                GetIPTVPlayerVersion(),
                offsetCoverX + tmpX * numOfCol + offsetCoverX - disWidth,  # width of status line
                offsetMarkerX, offsetMarkerY,  # first marker position
                markerWidth, markerHeight,    # marker size
                self.pageItemStartX, self.pageItemStartY,  # pagination marker
                self.pageItemSize, self.pageItemSize,
                offsetCoverX + tmpX * numOfCol + offsetCoverX - disWidth - 70,
            )

        for y in range(1, numOfRow + 1):
            for x in range(1, numOfCol + 1):
                skinCoverLine = """<widget name="cover_%s%s" zPosition="4" position="%d,%d" size="%d,%d" transparent="1" alphatest="blend" />""" % (
                    x, y,
                    (offsetCoverX + tmpX * (x - 1)),  # pos X image
                    (offsetCoverY + tmpY * (y - 1)),  # pos Y image
                    coverWidth,
                    coverHeight
                )
                skin += '\n' + skinCoverLine

        # add pagination items
        for pageItemOffset in range(self.numOfPages):
            pageItemX = self.pageItemStartX + pageItemOffset * self.pageItemSize
            skinCoverLine = """<ePixmap zPosition="2" position="%d,%d" size="%d,%d" pixmap="%s" transparent="1" alphatest="blend" />""" % (pageItemX, self.pageItemStartY, self.pageItemSize, self.pageItemSize, GetIconDir('radio_button_off.png'))
            skin += '\n' + skinCoverLine
        skin += '</screen>'
        self.skin = skin

        self.session = session
        Screen.__init__(self, session)

        self.session.nav.event.append(self.__event)
        self.onClose.append(self.__onClose)

        # load icons
        self.pixmapList = []
        for idx in range(0, self.numOfItems):
            self.pixmapList.append(LoadPixmap(GetIconDir('PlayerSelector/' + self.currList[idx][1] + '%i.png' % self.IconsSize)))

        self.markerPixmap = LoadPixmap(GetIconDir('PlayerSelector/marker%i.png' % self.MarkerSize))
        self.markerPixmapSel = LoadPixmap(GetIconDir('PlayerSelector/markerSel%i.png' % self.MarkerSize))
        self.pageMarkerPixmap = LoadPixmap(GetIconDir('radio_button_on.png'))
        # self.menuPixmap = LoadPixmap(GetIconDir('menu.png'))

        self["key_menu"] = StaticText(_("MENU"))
        self["key_red"] = StaticText(_("Sort Mode"))
        self["key_green"] = StaticText(_("More - Menu"))
        self["key_yellow"] = StaticText(_("Hide/Active Group"))
        self["key_blue"] = StaticText(_("Download manager"))

        self["actions"] = ActionMap(["IPTVPlayerListActions"],
        {
            "menu": self.keyMenu,
        }, -1)

        self["actions"] = ActionMap(["WizardActions", "DirectionActions", "ColorActions"],
        {
            "ok": self.ok_pressed,
            "back": self.back_pressed,
            "left": self.keyLeft,
            "right": self.keyRight,
            "up": self.keyUp,
            "down": self.keyDown,
            "blue": self.keyMenu,
            "red": self.changeReorderingMode,
            "green": self.keyBlue,
            "yellow": self.keyYellow,
        }, -1)
        self["marker"] = Cover3()
        self["page_marker"] = Cover3()
        # self['IptvVersion'] = Label(GetIPTVPlayerVersion())
        self["menu"] = Cover3()

        for y in range(1, self.numOfRow + 1):
            for x in range(1, self.numOfCol + 1):
                strIndex = "cover_%s%s" % (x, y)
                self[strIndex] = Cover3()

        self["statustext"] = Label(self.currList[0][0])

        self.onLayoutFinish.append(self.onStart)
        self.visible = True
        self.reorderingMode = False
        self.reorderingItemSelected = False

    def __del__(self):
        printDBG("PlayerSelectorWidget.__del__ --------------------------")

    def __onClose(self):
        self.session.nav.event.remove(self.__event)
        self.onClose.remove(self.__onClose)
        try:
            if self.reorderingMode and self.numOfLockedItems > 0:
                self.currList.extend(self.inList[len(self.inList) - self.numOfLockedItems:])

            if self.outList != self.currList:
                for item in self.currList:
                    self.outList.append(item)
        except Exception:
            printExc()
        idx = self.currLine * self.numOfCol + self.dispX
        printDBG(">>>>>>>>>>>>>>>>>>>>>>>>>>> __onClose idx[%s]" % idx)
        PlayerSelectorWidget.LAST_SELECTION[self.groupName] = idx

    # Calculate marker position Y
    def calcMarkerPosY(self):

        if self.currLine > (self.numOfLines - 1):
            self.currLine = 0
        elif self.currLine < 0:
            self.currLine = (self.numOfLines - 1)

        # calculate new page number
        newPage = int(self.currLine / self.numOfRow)
        if newPage != self.currPage:
            self.currPage = newPage
            self.updateIcons()

        # calculate dispY pos
        self.dispY = self.currLine - self.currPage * self.numOfRow

        # if we are in last line dispX pos
        # must be also corrected
        if self.currLine == (self.numOfLines - 1):
            self.numItemsInLine = self.numOfItems - ((self.numOfLines - 1) * self.numOfCol)
            if self.dispX > (self.numItemsInLine - 1):
                self.dispX = self.numItemsInLine - 1

        return

    # Calculate marker position X
    def calcMarkerPosX(self):
        if self.currLine == self.numOfLines - 1:
            # calculate num of item in last line
            self.numItemsInLine = self.numOfItems - ((self.numOfLines - 1) * self.numOfCol)
        else:
            self.numItemsInLine = self.numOfCol

        if self.dispX > (self.numItemsInLine - 1):
            self.dispX = 0
        elif self.dispX < 0:
            self.dispX = self.numItemsInLine - 1

        return

    def onStart(self):
        self.onLayoutFinish.remove(self.onStart)
        self["marker"].setPixmap(self.markerPixmap)
        self["page_marker"].setPixmap(self.pageMarkerPixmap)
        # self["menu"].setPixmap(self.menuPixmap)
        self.offsetCoverX = self['marker'].position[0] + (self.markerWidth - self.coverWidth) / 2
        self.offsetCoverY = self['marker'].position[1] + (self.markerHeight - self.coverHeight) / 2
        self.pageItemStartX = self['page_marker'].position[0]
        self.pageItemStartY = self['page_marker'].position[1]
        self.initDisplayList()
        return

    def reInitDisplayList(self):
        self.lastSelection = self.currLine * self.numOfCol + self.dispX
        self.calcDisplayVariables()
        self.initDisplayList()

    def initDisplayList(self):
        self.updateIcons()
        self.setIdx(self.lastSelection)

    def calcDisplayVariables(self):
        # numbers of items in self.currList
        self.numOfItems = len(self.currList)

        if self.lastSelection >= self.numOfItems:
            self.lastSelection = self.numOfItems - 1

        # numbers of lines
        self.numOfLines = int(self.numOfItems / self.numOfCol)
        if self.numOfItems % self.numOfCol > 0:
            self.numOfLines += 1

        # numbers of pages
        self.numOfPages = int(self.numOfLines / self.numOfRow)
        if self.numOfLines % self.numOfRow > 0:
            self.numOfPages += 1

        self.currPage = 0
        self.currLine = 0

        self.dispX = 0
        self.dispY = 0

    def updateIconsList(self, rangeList):
        idx = int(self.currPage * (self.numOfCol * self.numOfRow))
        for y in range(1, self.numOfRow + 1):
            for x in range(1, self.numOfCol + 1):
                if idx >= rangeList[0] and idx <= rangeList[1]:
                    strIndex = "cover_%s%s" % (x, y)
                    printDBG("updateIconsList [%s]" % strIndex)
                    self[strIndex].setPixmap(self.pixmapList[idx])
                idx += 1

    def updateIcons(self):
        idx = int(self.currPage * (self.numOfCol * self.numOfRow))
        for y in range(1, self.numOfRow + 1):
            for x in range(1, self.numOfCol + 1):
                strIndex = "cover_%s%s" % (x, y)
                printDBG("updateIcon for self[%s]" % strIndex)
                if idx < self.numOfItems:
                    # self[strIndex].updateIcon( resolveFilename(SCOPE_PLUGINS, 'Extensions/IPTVPlayer/icons/PlayerSelector/' + self.currList[idx][1] + '.png'))
                    self[strIndex].setPixmap(self.pixmapList[idx])
                    self[strIndex].show()
                    idx += 1
                else:
                    self[strIndex].hide()
        x = self.pageItemStartX + self.currPage * self.pageItemSize
        y = self.pageItemStartY
        self["page_marker"].instance.move(ePoint(int(x), y))

    def setIdx(self, selIdx):
        if selIdx > self.numOfItems:
            selIdx = self.numOfItems

        self.dispX = selIdx % self.numOfCol
        self.currLine = int(selIdx / self.numOfCol)

        self.calcMarkerPosX()
        self.calcMarkerPosY()
        self.moveMarker()
        return

    def keyRight(self):
        prev_idx = self.currLine * self.numOfCol + self.dispX
        self.dispX += 1
        self.calcMarkerPosX()
        self.moveMarker(prev_idx)
        return

    def keyLeft(self):
        prev_idx = self.currLine * self.numOfCol + self.dispX
        self.dispX -= 1
        self.calcMarkerPosX()
        self.moveMarker(prev_idx)
        return

    def keyDown(self):
        prev_idx = self.currLine * self.numOfCol + self.dispX
        self.currLine += 1
        self.calcMarkerPosY()
        self.moveMarker(prev_idx)
        return

    def keyUp(self):
        prev_idx = self.currLine * self.numOfCol + self.dispX
        self.currLine -= 1
        self.calcMarkerPosY()
        self.moveMarker(prev_idx)
        return

    def moveMarker(self, prev_idx=0):
        new_idx = int(self.currLine * self.numOfCol + self.dispX)

        if self.reorderingItemSelected:
            if prev_idx != new_idx:
                prevHost = self.currList[prev_idx]
                prevPixmap = self.pixmapList[prev_idx]
                del self.currList[prev_idx]
                del self.pixmapList[prev_idx]

                self.currList.insert(new_idx, prevHost)
                self.pixmapList.insert(new_idx, prevPixmap)
                self.updateIconsList(sorted([prev_idx, new_idx]))

        # calculate position of image
        imgPosX = self.offsetCoverX + (self.coverWidth + self.disWidth) * self.dispX
        imgPosY = self.offsetCoverY + (self.coverHeight + self.disHeight) * self.dispY

        # calculate postion of marker for current image
        x = int(imgPosX - (self.markerWidth - self.coverWidth) / 2)
        y = int(imgPosY - (self.markerHeight - self.coverHeight) / 2)

        # x =  30 + self.dispX * 180
        # y = 130 + self.dispY * 125
        self["marker"].instance.move(ePoint(x, y))
        self["statustext"].setText(self.currList[new_idx][0])
        return

    def getSelectedItem(self):
        printDBG(">> PlayerSelectorWidget.getSelectedItem")
        idx = self.currLine * self.numOfCol + self.dispX
        if idx < self.numOfItems:
            return self.currList[idx]
        return None

    def back_pressed(self):
        self.close(None)
        return

    def ok_pressed(self):
        if self.reorderingMode:
            if self.reorderingItemSelected:
                self["marker"].setPixmap(self.markerPixmap)
                self.reorderingItemSelected = False
            else:
                self["marker"].setPixmap(self.markerPixmapSel)
                self.reorderingItemSelected = True
            return

        idx = int(self.currLine * self.numOfCol + self.dispX)
        PlayerSelectorWidget.LAST_SELECTION[self.groupName] = idx

        if idx < self.numOfItems:
            self.close(self.currList[idx])
        else:
            self.close(None)
        return

    def keyBlue(self):
        self.close((_("Download manager"), "IPTVDM"))

    def keyYellow(self):
        """add lululla """
        self.close((_("Disable/Enable groups"), "config_groups"))

    def keyMenu(self):
        printDBG(">> PlayerSelectorWidget.keyMenu")
        options = []
        selItem = self.getSelectedItem()
        if self.groupObj is not None and selItem is not None and len(self.groupObj.getGroupsWithoutHost(selItem[1])):
            options.append((_("Add host %s to group") % selItem[0], "ADD_HOST_TO_GROUP"))

        if not self.reorderingMode and self.numOfItems - self.numOfLockedItems > 0:
            options.append((_("Enable reordering mode"), "CHANGE_REORDERING_MODE"))
        elif self.reorderingMode:
            options.append((_("Disable reordering mode"), "CHANGE_REORDERING_MODE"))
        options.append((_("Download manager"), "IPTVDM"))
        if self.groupName in ['selecthost', 'all']:
            options.append((_("Disable/Enable services"), "config_hosts"))
        if self.groupName in ['selectgroup']:
            options.append((_("Disable/Enable groups"), "config_groups"))

        if self.groupName == 'selecthost':
            pass
        elif self.groupName == 'selectgroup':
            if selItem[1] not in ['update', 'config', 'all']:
                options.append((_('Hide "%s" group') % selItem[0], "DEL_ITEM"))
        elif self.groupName not in ['all']:
            options.append((_('Remove "%s" item') % selItem[0], "DEL_ITEM"))

        if len(options):
            self.session.openWithCallback(self.selectMenuCallback, ChoiceBox, title=_("Select option"), list=options)

    def selectMenuCallback(self, ret):
        printDBG(">> PlayerSelectorWidget.selectMenuCallback")
        if ret:
            ret = ret[1]
            if ret == "CHANGE_REORDERING_MODE":
                self.changeReorderingMode()
            elif ret == "IPTVDM":
                self.keyBlue()
            elif ret in ["config_hosts", "config_groups"]:
                self.close((_("Disable not used services"), ret))
            elif ret == "ADD_HOST_TO_GROUP":
                self.addHostToGroup()
            elif ret == 'DEL_ITEM':
                idx = self.currLine * self.numOfCol + self.dispX
                if idx < self.numOfItems:
                    del self.currList[idx]
                    del self.pixmapList[idx]
                    self.reInitDisplayList()

    def addHostToGroup(self):
        printDBG(">> PlayerSelectorWidget.addHostToGroup")
        selItem = self.getSelectedItem()
        if selItem is None:
            printDBG("No selected item")
            return
        if len(selItem) < 2:
            printDBG("Selected item too short: %s" % str(selItem))
            return
        if self.groupObj is None:
            printDBG("groupObj is None")
            return

        groupsList = self.groupObj.getGroupsWithoutHost(selItem[1])
        options = []
        for item in groupsList:
            options.append((item.title, item.name))

        if len(options):
            self.session.openWithCallback(self.addHostToGroupCallback, ChoiceBox, title=_("Select group"), list=options)

    def addHostToGroupCallback(self, ret):
        if ret:
            ret = ret[1]
            selItem = self.getSelectedItem()
            self.groupObj.addHostToGroup(ret, selItem[1])

    def changeReorderingMode(self):
        printDBG(">> PlayerSelectorWidget.changeReorderingMode")
        if not self.reorderingMode and (self.numOfItems - self.numOfLockedItems) > 0:
            self.reorderingMode = True
            if self.numOfLockedItems > 0:
                self.currList = self.currList[:self.numOfLockedItems * -1]
                self.reInitDisplayList()
        else:
            if self.reorderingItemSelected:
                self["marker"].setPixmap(self.markerPixmap)
            self.reorderingMode = False
            if self.numOfLockedItems > 0:
                self.currList.extend(self.inList[len(self.inList) - self.numOfLockedItems:])
                self.reInitDisplayList()

        self.reorderingItemSelected = False

    def hideWindow(self):
        self.visible = False
        self.hide()

    def showWindow(self):
        self.visible = True
        self.show()

    def Error(self, error=None):
        pass

    def __event(self, ev):
        pass
