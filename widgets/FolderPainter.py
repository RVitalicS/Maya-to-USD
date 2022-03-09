#!/usr/bin/env python



from . import tools
from .paintblock import (
    clear,
    label
)


from Qt import QtCore, QtGui
from . import ItemBase

from . import Settings
UIGlobals = Settings.UIGlobals





class Base (object):


    def __init__ (self):

        self.folderNameArea  = QtCore.QRect()
        self.createFolderArea = QtCore.QRect()

        self.linkArea = QtCore.QRect()

        self.controlMode = False



    @label(UIGlobals.IconDelegate.fontCategory)
    @clear
    def paintLabel (self):
        pass



    def paintFolder (self):

        # BACKGROUND
        self.painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        if self.hover:
            color = QtGui.QColor(self.theme.iconHilight)
        else:
            color = QtGui.QColor(self.theme.iconBackground)
        self.painter.fillRect(self.iconRect, color)


        # ICON
        folderImage = QtGui.QImage(":/icons/folder.png")

        folderOffset = int((
            self.height - self.space*2 - folderImage.height() )/2)

        folderPosition = QtCore.QPoint(
                self.iconRect.x() + folderOffset,
                self.iconRect.y() + folderOffset)
        
        folderImage = tools.recolor(folderImage, self.theme.folderColor)
        self.painter.drawImage(folderPosition, folderImage)


        # NAME
        self.painter.setRenderHint(QtGui.QPainter.TextAntialiasing, True)
        self.painter.setPen(
            QtGui.QPen(
                QtGui.QBrush( QtGui.QColor(self.theme.text) ),
                0,
                QtCore.Qt.SolidLine,
                QtCore.Qt.RoundCap,
                QtCore.Qt.RoundJoin) )

        offsetText = 1
        self.painter.setFont( UIGlobals.IconDelegate.fontFolderName )

        offsetName = folderImage.width() + folderOffset*2
        self.folderNameArea = QtCore.QRect(
            self.pointX + self.space + offsetName   ,
            self.pointY + self.space ,
            self.width  - self.space*2 - offsetName ,
            int(self.height/2) - int(self.space/2) -offsetText )


        name = self.data.get("name")

        textOption = QtGui.QTextOption()
        textOption.setWrapMode(QtGui.QTextOption.NoWrap)
        textOption.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignBottom)

        self.painter.drawText(
            QtCore.QRectF(self.folderNameArea),
            name,
            textOption)


        # ITEMS
        self.painter.setPen(
            QtGui.QPen(
                QtGui.QBrush( QtGui.QColor(self.theme.textlock) ),
                0,
                QtCore.Qt.SolidLine,
                QtCore.Qt.RoundCap,
                QtCore.Qt.RoundJoin) )

        self.painter.setFont( UIGlobals.IconDelegate.fontFolderItems )

        offsetName = folderImage.width() + folderOffset*2
        countArea = QtCore.QRect(
            self.pointX + self.space + offsetName   ,
            self.pointY + int(self.height/2) +offsetText ,
            self.width  - self.space*2 - offsetName ,
            int(self.height/2) )


        count = self.data.get("items")
        if count == 1:
            text = "1 item"
        elif count > 1:
            text = "{} items".format(count)
        else:
            text = "empty"

        textOption = QtGui.QTextOption()
        textOption.setWrapMode(QtGui.QTextOption.NoWrap)
        textOption.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)

        self.painter.drawText(
            QtCore.QRectF(countArea),
            text,
            textOption)


        # LINK
        if self.hover and self.controlMode and name != "":

            linkImage = QtGui.QImage(":/icons/link.png")
            linkImage = tools.recolor(linkImage, self.theme.kicker, opacity=0.25)

            linkOffset = linkImage.width() + UIGlobals.IconDelegate.offsetLink

            linkPosition = QtCore.QPoint(
                    self.iconRect.x() + self.iconRect.width()  - linkOffset,
                    self.iconRect.y() + self.iconRect.height() - linkOffset)

            self.painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            self.painter.drawImage(linkPosition, linkImage)

            self.linkArea = QtCore.QRect(
                linkPosition.x() ,
                linkPosition.y() ,
                linkImage.width() ,
                linkImage.height() )



    def paintPlus (self):

        self.painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        libraryImage = QtGui.QImage(":/icons/plus.png")

        offsetIcon = int((
            self.height - self.space*2 - libraryImage.height() )/2)

        iconPosition = QtCore.QPoint(
                self.pointX + self.space + offsetIcon,
                self.pointY + self.space + offsetIcon)

        self.createFolderArea = QtCore.QRect(
            iconPosition.x() ,
            iconPosition.y() ,
            libraryImage.width() ,
            libraryImage.height() )

        if self.createFolderArea.contains(self.pointer):
            libraryImage = tools.recolor(libraryImage, self.theme.plusHover)
        else:
            libraryImage = tools.recolor(libraryImage, self.theme.plusColor)

        self.painter.drawImage(iconPosition, libraryImage)






class Item (ItemBase.Painter, Base):


    def __init__ (self, theme):
        ItemBase.Painter.__init__(self, theme)
        Base.__init__(self)


    def paint (self, painter, option, index):
        super(Item, self).paint(painter, option, index)

        if self.type == "labelfolder":
            self.paintLabel()

        elif self.type in [
                "folder"      ,
                "folderquery" ]:
            self.paintFolder()

        elif self.type == "plusfolder":
            self.paintPlus()
