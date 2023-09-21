from math import *
from pygame import *
import pygame
from pyperclip import *
from os import *
from time import time_ns

pygame.init()

#Nombre de widget existants
_nbWidget = 0

###################### Base widget class
class MWidget:
    def __init__(self, x, y, width, height, parent, widgetType = "MWidget"): #MWidget's constructor
        global _nbWidget
        self.backgroundColor = (255, 255, 255)
        self.cursorOnOverflight = pygame.SYSTEM_CURSOR_ARROW
        self.focused = False
        self.height = height
        self.mouseDown = -1
        self.mouseUp = -1
        self.overflighted = False
        self.parent = 0
        self.setShouldModify(True)
        self.visible = True
        self.width = width
        self.x = x
        self.y = y
        self._BACKGROUNDCOLOR = self.backgroundColor
        self._children = []
        self._id = _nbWidget
        self._lastSurface = 0
        self._type = widgetType

        _nbWidget += 1

        if parent != 0:
            self.setParent(parent)

        if self._type != "MApp": #Register the widget into the MApp object
            self.parent._declaringWidget(self)

    def absolutePos(self): #Return the pos according to the MApp object
        return self.absoluteX(), self.absoluteY()
    
    def absoluteX(self): #Return x according to the MApp object
        if self._type == "MApp":
            return 0
        else:
            x = self.getX()
            x += self.parent.absoluteX()
            return x
        
    def absoluteY(self): #Return y according to the MApp object
        if self._type == "MApp":
            return 0
        else:
            y = self.getY()
            y += self.parent.absoluteY()
            return y

    def containsChild(self, id): #Return if the widget contains the child with the id
        for i1, i2 in enumerate(self._children): #Search through all the children to find the one with the good id
            if i2.getID() == id:
                return i1
        return -1
    
    def getBackgroundColor(self): #Return the value of backgroundColor
        return self.backgroundColor
    
    def getChildren(self): #Report the list of all the children of the widget
        return self._children
    
    def getChildrenAtIndex(self, index): #Report the widget at the index "index" in the list _children
        return self._children[index]
    
    def getCursorOnOverflight(self): #Return the value of cursorOnOverflight
        return self.cursorOnOverflight
    
    def getFocused(self): #Return the value of focused
        return self.focused

    def getHeight(self): #Return the value of height
        return self.height
    
    def getID(self): #Return the value of _id
        return self._id
    
    def getMouseDown(self): #Return the value of mouseDown
        return self.mouseDown
    
    def getMouseUp(self): #Return the value of mouseUp
        return self.mouseUp
    
    def getOverflighted(self): #Return if the widget is overflighted or not
        return self.overflighted

    def getParent(self): #Return the value of parent
        return self.parent
    
    def getRect(self): #Return (x, y, width, height)
        return (self.getX(), self.getY(), self.getWidth(), self.getHeight())
    
    def getShouldModify(self): #Return the value of should modify
        return self.shouldModify
    
    def getVisible(self): #Return the value of visible
        return self.visible
    
    def getWidth(self): #Return the value of width
        return self.width
    
    def getX(self): #Return the value of X
        return self.x
    
    def getY(self): #Return the value of Y
        return self.y
    
    def move(self, newX, newY): #Change the value of X and Y in one function
        self.setX(newX)
        self.setY(newY)

    def posIn(self, pos): #Check if "pos" is in the widget
        if pos[0] >= self.absoluteX() and pos[1] > self.absoluteY() and pos[0] < self.absoluteX() + self.getWidth() and pos[1] < self.absoluteY() + self.getHeight():
            return True
        return False
    
    def resetWidget(self): #Reset the widget as its initial state (with no events)
        self.backgroundColor = self._BACKGROUNDCOLOR
        self.setShouldModify(True)

    def resize(self, newWidth, newHeight): #Change the value of width and height in one function
        self.setHeight(newHeight)
        self.setWidth(newWidth)

    def setBackgroundColor(self, backgroundColor, constant = True): #Change the value of backgroundColor
        if not (self.backgroundColor == self._BACKGROUNDCOLOR and self.backgroundColor == backgroundColor):
            self.backgroundColor = backgroundColor
            if constant:
                self._BACKGROUNDCOLOR = backgroundColor
            else:
                if self._type == "MApp":
                    self._addWidgetToReset(self)
                else:
                    self._mapp._addWidgetToReset(self)
            self.setShouldModify(True)

    def setCursorOnOverflight(self, cursorOnOverflight): #Return the value of cursorOnOverflight
        self.cursorOnOverflight = cursorOnOverflight
    
    def setHeight(self, newHeight): #Change the value of height
        self.height = newHeight
        self.setShouldModify(True)
    
    def setParent(self, newParent): #Change the value of parent
        if self.parent != 0:
            self.parent._removeChild(self)

        self.parent = newParent
        self.setShouldModify(True)

        newParent._addChild(self)

    def setShouldModify(self, shouldModify): #Change the value of shouldModify
        if shouldModify:
            self.shouldModify = True
            if self.parent != 0:
                self.parent.setShouldModify(True)
        else:
            self.shouldModify = False
            
    def setVisible(self, visible): #Return the value of visible
        if visible != self.visible:
            self.visible = visible
            self.setShouldModify(True)

    def setWidth(self, newWidth): #Change the value of width
        self.width = newWidth
        self.setShouldModify(True)

    def setX(self, newX): #Change the value of X
        self.x = newX
        self.setShouldModify(True)

    def setY(self, newY): #Change the value of Y
        self.y = newY
        self.setShouldModify(True)

    def softResetWidget(self): #Reset without graphics modification
        self.mouseDown = -1
        self.mouseUp = -1
        self.overflighted = False

    def _addChild(self, child): #Add a child to the widget
        if self.containsChild(child.getID()) == -1:
            self._children.append(child)

    def _declaringWidget(self, widget): #Declare widget to the MApp if the widget is a MApp (function defined in MApp) or pass hit to his parent
        self.parent._declaringWidget(widget)

    def _isGettingMouseDown(self, button, relativePos): #Function usefull for heritage, call by MApp when the widget is clicked (called for only one frame) with button = left button (1) and right button (2)
        pass

    def _isGettingMouseUp(self, button, relativePos): #Function usefull for heritage, call by MApp when the widget is stopping of being clicked (called for only one frame) with button = left button (1) and right button (2)
        pass

    def _isGettingOverflighted(self): #Function usefull for heritage, call by MApp when the widget is overflighted (applicated for only one frame)
        pass

    def _isKeyGettingDropped(self, key): #Function usefull for heritage, call by MApp when the widget is focused and a key is dropped on the keyboard (applicated for only one frame)
        pass

    def _isKeyGettingPressed(self, key): #Function usefull for heritage, call by MApp when the widget is focused and a key is pressed on the keyboard (applicated for only one frame)
        pass

    def _isNotFocusedAnymore(self): #Function usefull for heritage, call by MApp when the widget is not focused anymore
        pass

    def _isTextGettingEntered(self, text): #Function usefull for heritage, call by MApp when the widget is focused and the user is typing a text
        pass
    
    def _mouseMove(self, buttons, pos, relativeMove): #Function usefull for heritage, call by MApp when the widget is focused and the mouse is moved
        pass

    def _removeChild(self, child): #Remove a child to the widget
        id = self.containsChild(child.getId())
        if id != -1:
            self._children = self._children[:id] + self._children[id:]

    def _render(self): #Render widget and return rendering

        if self.getShouldModify(): #If the widget should do the render, do it
            widgetSurface = Surface((self.width, self.height), pygame.SRCALPHA)

            widgetSurface.blit(self._renderBeforeHierarchy(widgetSurface), (0, 0, self.getWidth(), self.getHeight()))
            widgetSurface.blit(self._renderHierarchy(widgetSurface), (0, 0, self.getWidth(), self.getHeight()))
            widgetSurface.blit(self._renderAfterHierarchy(widgetSurface), (0, 0, self.getWidth(), self.getHeight()))

            self._lastSurface = widgetSurface #Store the last generated surface into _lastSurface

            self.setShouldModify(False) #Update shouldModify
            return widgetSurface
        #Else, use _lastSurface
        return self._lastSurface
    
    def _renderAfterHierarchy(self, surface): #Render widget on surface after hierarchy render
        return surface
    
    def _renderBeforeHierarchy(self, surface): #Render widget on surface before hierarchy render
        surface.fill(self.backgroundColor, (0, 0, self.getWidth(), self.getHeight()))
        return surface
    
    def _renderHierarchy(self, surface): #Render hierarchy on surface
        for child in self._children: #Get the _render of all the children
            if child.getVisible():
                surface.blit(child._render(), child.getRect())
        return surface
    
    def _update(self, deltaTime): #Function usefull for heritage, call by MApp every frame
        pass

###################### Main application class
class MApp(MWidget):
    def __init__(self, pygameWindow, windowTitle, windowWidth, windowHeight, printFps = False): #MApp's constructor
        MWidget.__init__(self, 0, 0, windowWidth, windowHeight, 0, "MApp") #Parent class constructor call
        self.deltaTime = 0
        self.focusedWidget = self
        self.fps = 0
        self.pressedKey = []
        self.printFps = printFps
        self.setWindowTitle(windowTitle)
        self._deltaTimeCache = time_ns()
        self._fpsCount = 0
        self._fpsDuration = 0
        self._modifiedWidget = []
        self._pygameWindow = pygameWindow
        self._widgets = []

    def frame(self): #Do a frame in the application
        self.frameEvent()
        self.frameGraphics()

    def frameEvent(self): #Do all events updates in the application
        self.deltaTime = (time_ns() - self._deltaTimeCache)/(10**9)
        self._deltaTimeCache = time_ns() #Calculate deltaTime

        self._fpsDuration += self.deltaTime
        if self._fpsDuration >= 1: #Handle fps counting
            self.fps = self._fpsCount
            self._fpsDuration -= 1
            self._fpsCount = 0

            if self.printFps:
                print(self.fps)

        self._fpsCount += 1

        self.pressedKey.clear()

        for i in self._widgets: #Soft reset all widget
            i.softResetWidget()
            i._update(self.getDeltaTime())

        for i in self._modifiedWidget: #Reset all modified widget in the last call of frameEvent
            i.resetWidget()

        self._modifiedWidget.clear()

        cursor = self.getCursorOnOverflight()

        mousePos = pygame.mouse.get_pos() #Get mouse position

        overflightedWidget = self
        i = 0
        while i < len(overflightedWidget.getChildren()): #Find the overflighted widget
            widget = overflightedWidget.getChildrenAtIndex(i)
            if widget.posIn(mousePos):
                overflightedWidget = widget
                i = -1
            i += 1

        cursor = overflightedWidget.getCursorOnOverflight()
        overflightedWidget.overflighted = True
        pygame.mouse.set_cursor(cursor)
        overflightedWidget._isGettingOverflighted()

        events = pygame.event.get()
        for event in events: #Event handler
            if event.type == pygame.QUIT: #Quit pygame
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN: #If the mouse is clicked
                overflightedWidget.mouseDown = event.button
                self.focusedWidget.focused = False
                self.focusedWidget._isNotFocusedAnymore()
                self.focusedWidget = overflightedWidget
                self.focusedWidget.focused = True
                overflightedWidget._isGettingMouseDown(event.button, (event.pos[0] - overflightedWidget.getX(), event.pos[1] - overflightedWidget.getY()))
            elif event.type == pygame.MOUSEBUTTONUP: #If the mouse is stopping of being clicked
                overflightedWidget.mouseUp = event.button
                overflightedWidget._isGettingMouseUp(event.button, (event.pos[0] - overflightedWidget.getX(), event.pos[1] - overflightedWidget.getY()))
            elif event.type == pygame.MOUSEMOTION: #If hte mouse is moving
                self.focusedWidget._mouseMove(event.buttons, (event.pos[0] - self.focusedWidget.getX(), event.pos[1] - self.focusedWidget.getY()), event.rel)
            elif event.type == pygame.KEYDOWN: #If a key is pressed on the keyboard
                self.focusedWidget._isKeyGettingPressed(event.key)
                self.pressedKey.append(event.key)
            elif event.type == pygame.KEYUP: #If a key is dropped on the keyboard
                self.focusedWidget._isKeyGettingDropped(event.key)
            elif event.type == pygame.TEXTINPUT: #If the user is enterring text
                self.focusedWidget._isTextGettingEntered(event.text)

    def frameGraphics(self): #Do all graphics updates in the application
        self._pygameWindow.blit(self._render(), (0, 0, self.width, self.height))

    def getDeltaTime(self): #Return deltaTime
        return self.deltaTime
    
    def getFps(self): #Return fps
        return self.fps
    
    def getPressedKey(self): #Return pressedKey
        return self.pressedKey
    
    def getPrintFps(self): #Return printFps
        return self.printFps
    
    def getWidgets(self): #Return _widget
        return self._widgets
    
    def isKeyPressed(self, key): #Return if the key is pressed
        for i in self.pressedKey:
            if key == i:
                return True
        return False
    
    def setPrintFps(self, printFps): #Change the value of printFps
        self.printFps = printFps

    def setWindowTitle(self, windowTitle): #Change the title of the window
        self.windowTitle = windowTitle

        pygame.display.set_caption(windowTitle)

    def _addWidgetToReset(self, widget): #Add a widget _modifiedWidget
        self._modifiedWidget.append(widget)

    def _containsWidget(self, widget): #Return if a widget is stored into _widgets
        for i in self._widgets:
            if i.getID() == widget.getID():
                return True
        return False

    def _declaringWidget(self, widget): #Declare widget to the MApp if the widget is a MApp or pass hit to his parent (function defined in MWidget)
        if not self._containsWidget(widget):
            self._widgets.append(widget)
            widget._mapp = self

###################### Usefull class to do widget with frame
class MFrame(MWidget):
    def __init__(self, x, y, width, height, parent, widgetType = "MFrame"):
        super().__init__(x, y, width, height, parent, widgetType)

        self.frameBeforeHierarchy = True
        self.frameBottomWidth = 0
        self.frameColor = (0, 0, 0)
        self.frameLeftWidth = 0
        self.frameRightWidth = 0
        self.frameTopWidth = 0
        self.leftBottomCornerRadius = 0
        self.leftTopCornerRadius = 0
        self.rightBottomCornerRadius = 0
        self.rightTopCornerRadius = 0

    def getCornerRadius(self, index = 0): #Return the value of leftTopCornerRadius if 0, leftBottomCornerRadius if 1, rightBottomCornerRadius if 2, rightTopCornerRadius if 3
        if index == 0:
            return self.leftTopCornerRadius
        elif index == 1:
            return self.leftBottomCornerRadius
        elif index == 2:
            return self.rightBottomCornerRadius
        else:
            return self.rightTopCornerRadius

    def getFrameBeforeHierarchy(self): #Return the value of frameBeforeHierarchy
        return self.frameBeforeHierarchy
    
    def getFrameColor(self): #Return frameColor
        return self.frameColor
    
    def getFrameWidth(self, index = 0): #Return the value of frameBottomWidth if 1, frameLeftWidth if 2, frameRightWidth if 3, frameTopWidth if 4
        if index == 0:
            return self.frameTopWidth
        elif index == 1:
            return self.frameLeftWidth
        elif index == 2:
            return self.frameBottomWidth
        else:
            return self.frameRightWidth
        
    def setCornerRadius(self, cornerRadius, index = -1): #Return the value of leftTopCornerRadius if 0, leftBottomCornerRadius if 1, rightBottomCornerRadius if 2, rightTopCornerRadius if 3
        if index == 0:
            if self.leftTopCornerRadius != cornerRadius:
                print(self.leftTopCornerRadius, cornerRadius)
                self.leftTopCornerRadius = cornerRadius
                self.setShouldModify(True)
        elif index == 1:
            if self.leftBottomCornerRadius != cornerRadius:
                self.leftBottomCornerRadius = cornerRadius
                self.setShouldModify(True)
        elif index == 2:
            if self.rightBottomCornerRadius != cornerRadius:
                self.rightBottomCornerRadius = cornerRadius
                self.setShouldModify(True)
        elif index == 3:
            if self.rightTopCornerRadius != cornerRadius:
                self.rightTopCornerRadius = cornerRadius
                self.setShouldModify(True)
        else:
            if not (self.leftTopCornerRadius == cornerRadius and self.leftBottomCornerRadius == cornerRadius and self.rightBottomCornerRadius == cornerRadius and self.rightTopCornerRadius == cornerRadius):
                self.leftTopCornerRadius = cornerRadius
                self.leftBottomCornerRadius = cornerRadius
                self.rightBottomCornerRadius = cornerRadius
                self.rightTopCornerRadius = cornerRadius
                self.setShouldModify(True)
    
    def setFrameBeforeHierarchy(self, frameBeforeHierarchy): #Change the value of frameBeforeHierarchy
        if self.frameBeforeHierarchy != frameBeforeHierarchy:
            self.frameBeforeHierarchy = frameBeforeHierarchy
            self.setShouldModify(True)

    def setFrameColor(self, color): #Change the value of frameColor
        if self.frameColor != color:
            self.frameColor = color
            self.setShouldModify(True)

    def setFrameWidth(self, frameWidth, index = -1): #Change the value of frameBottomWidth if 1, frameLeftWidth if 2, frameRightWidth if 3, frameTopWidth if 4
        if index == 0:
            if self.frameTopWidth != frameWidth:
                self.frameTopWidth = frameWidth
                self.setShouldModify(True)
        elif index == 1:
            if self.frameLeftWidth != frameWidth:
                self.frameLeftWidth = frameWidth
                self.setShouldModify(True)
        elif index == 2:
            if self.frameBottomWidth != frameWidth:
                self.frameBottomWidth = frameWidth
                self.setShouldModify(True)
        elif index == 3:
            if self.frameRightWidth != frameWidth:
                self.frameRightWidth = frameWidth
                self.setShouldModify(True)
        else:
            if not (self.frameTopWidth == frameWidth and self.frameLeftWidth == frameWidth and self.frameBottomWidth == frameWidth and self.frameRightWidth == frameWidth):
                self.frameBottomWidth = frameWidth
                self.frameLeftWidth = frameWidth
                self.frameRightWidth = frameWidth
                self.frameTopWidth = frameWidth
                self.setShouldModify(True)

    def _renderAfterHierarchy(self, surface): #Render widget on surface after hierarchy render
        if not self.frameBeforeHierarchy:
            pygame.draw.rect(surface, self.frameColor, (0, 0, self.getWidth(), self.getHeight()), 0, 0, self.leftTopCornerRadius, self.rightTopCornerRadius, self.leftBottomCornerRadius, self.rightBottomCornerRadius)
        return surface

    def _renderBeforeHierarchy(self, surface): #Render widget on surface before hierarchy render
        if self.frameBeforeHierarchy:
            pygame.draw.rect(surface, self.frameColor, (0, 0, self.getWidth(), self.getHeight()), 0, 0, self.leftTopCornerRadius, self.rightTopCornerRadius, self.leftBottomCornerRadius, self.rightBottomCornerRadius)
        pygame.draw.rect(surface, self.backgroundColor, (self.getFrameWidth(1), self.getFrameWidth(0), self.getWidth() - (self.getFrameWidth(1) + self.getFrameWidth(3)), self.getHeight() - (self.getFrameWidth(0) + self.getFrameWidth(2))), 0, 0, self.leftTopCornerRadius, self.rightTopCornerRadius, self.leftBottomCornerRadius, self.rightBottomCornerRadius)
        return surface

###################### Usefull class to display image
class MImage(MFrame):
    def __init__(self, imageLink, x, y, width, height, parent, widgetType = "MImage"):
        super().__init__(x, y, width, height, parent, widgetType)

        self.imageHorizontalAlignment = 0
        self.imageLink = ""
        self.imagePosition = (0, 0)
        self.imageReframing = 0
        self.imageSize = (0, 0)
        self.imageVerticalAlignment = 0
        self._image = 0

        self.setImageLink(imageLink)

    def getImageHorizontalAlignment(self): #Return "imageAlignment"
        return self.imageHorizontalAlignment

    def getImageLink(self): #Return "imageLink"
        return self.imageLink
    
    def getImagePosition(self): #Return "imagePosition"
        return self.imagePosition
    
    def getImageReframing(self): #Return "imageReframing"
        return self.imageReframing
    
    def getImageSize(self): #Return "imageSize"
        return self.imageSize
    
    def getImageVerticalAlignment(self): #Return "imageVerticalAlignment"
        return self.imageVerticalAlignment
    
    def setImageHorizontalAlignment(self, imageHorizontalAlignment): #Change "imageAlignment"
        if imageHorizontalAlignment != self.imageHorizontalAlignment:
            self.imageHorizontalAlignment = imageHorizontalAlignment
            self.setShouldModify(True)
    
    def setImageLink(self, imageLink, editSize = True): #Change "imageLink"
        if path.exists(imageLink):
            if imageLink != self.imageLink:
                self.imageLink = imageLink
                self._image = image.load(imageLink)
                self._imageToDraw = self._image

                if editSize:
                    self.imageSize = self._image.get_size()
                self._resizeImage()
                self.setShouldModify(True)
        else:
            print("Attention, l'image au lien ", imageLink, "n'existe pas.")

    def setImagePosition(self, imagePosition): #Change "imagePosition"
        if imagePosition != self.imagePosition:
            self.imagePosition = imagePosition
            if self.getImageHorizontalAlignment() == -1 or self.getImageVerticalAlignment() == -1:
                self.setShouldModify(True)

    def setImageReframing(self, imageReframing): #Change imageReframing
        if self.imageReframing != imageReframing:
            self.imageReframing = imageReframing
            self._resizeImage()
            self.setShouldModify(True)

    def setImageSize(self, imageSize): #Change imageSize
        if self.imageSize != imageSize:
            self.imageSize = imageSize
            if self.getImageReframing() == 4:
                self._resizeImage()
                self.setShouldModify(True)

    def setImageVerticalAlignment(self, imageVerticalAlignment): #Change imageVerticalAlignment
        if imageVerticalAlignment != self.imageVerticalAlignment:
            self.imageVerticalAlignment = imageVerticalAlignment
            self.setShouldModify(True)

    def _renderBeforeHierarchy(self, surface): #Render widget on surface before hierarchy render
        surface = super()._renderBeforeHierarchy(surface)

        if self._image != 0:
            imageToDraw = self._imageToDraw
            x = 0
            y = 0

            if self.getImageHorizontalAlignment() == -1:
                x = self.getImagePosition()[0]
            elif self.getImageHorizontalAlignment() == 0:
                x = self.getFrameWidth(1)
            elif self.getImageHorizontalAlignment() == 1:
                x = self.getWidth()/2 - imageToDraw.get_width()/2
            else:
                x = self.getWidth() - (self.getFrameWidth(3) + imageToDraw.get_width())

            if self.getImageVerticalAlignment() == -1:
                y = self.getImagePosition()[1]
            elif self.getImageVerticalAlignment() == 0:
                y = self.getFrameWidth(0)
            elif self.getImageVerticalAlignment() == 1:
                y = self.getHeight()/2 - imageToDraw.get_height()/2
            else:
                y = self.getHeight() - (self.getFrameWidth(2) + imageToDraw.get_height())

            surface.blit(imageToDraw, (x, y, imageToDraw.get_width(), imageToDraw.get_height()))

        return surface

    def _resizeImage(self): #Resize image (only with reframing)
        if self.getImageReframing() != 0:
            if self.getImageReframing() == 1:
                resizeNumber = (self.getWidth() - (self.getFrameWidth(1) + self.getFrameWidth(3)))/self._image.get_width()
                self._imageToDraw = transform.scale(self._image, (self._image.get_width() * resizeNumber, self._image.get_height() * resizeNumber))
            elif self.getImageReframing() == 2:
                resizeNumber = (self.getHeight() - (self.getFrameWidth(0) + self.getFrameWidth(2)))/self._image.get_height()
                self._imageToDraw = transform.scale(self._image, (self._image.get_width() * resizeNumber, self._image.get_height() * resizeNumber))
            elif self.getImageReframing() == 3:
                resizeNumberW = (self.getWidth() - (self.getFrameWidth(1) + self.getFrameWidth(3)))/self._image.get_width()
                resizeNumberH = (self.getHeight() - (self.getFrameWidth(0) + self.getFrameWidth(2)))/self._image.get_height()
                self._imageToDraw = transform.scale(self._image, (self._image.get_width() * resizeNumberW, self._image.get_height() * resizeNumberH))
            else:
                resizeNumberW = self.getImageSize()[0]/self._image.get_width()
                resizeNumberH = self.getImageSize()[1]/self._image.get_height()
                self._imageToDraw = transform.scale(self._image, (self._image.get_width() * resizeNumberW, self._image.get_height() * resizeNumberH))
            self.setShouldModify(True)

###################### Usefull class to use text
class MText(MFrame):
    def __init__(self, text, x, y, width, height, parent, widgetType = "MText"):
        super().__init__(x, y, width, height, parent, widgetType)

        self.cursorPosition = 0
        self.cursorVisible = False
        self.cursorWidth = 2
        self.dynamicTextCut = False
        self.dynamicTextCutType = 1
        self.font = "arial"
        self.fontSize = 12
        self.input = False
        self.selection = False
        self.selectionBackgroundColor = (25, 102, 255)
        self.selectionStart = 0
        self.selectionStop = 0
        self.selectionTextColor = (0, 0, 0)
        self.text = text
        self.textBottomOffset = 0
        self.textColor = (0, 0, 0)
        self.textHorizontalAlignment = 0
        self.textLeftOffset = 0
        self.textRightOffset = 0
        self.textTopOffset = 0
        self.textVerticalAlignment = 0
        self._backspacePressed = False
        self._backspacePressedTime = 0
        self._backspaceNumber = 0
        self._baseSelection = 0
        self._bottomArrowPressed = False
        self._bottomArrowPressedAtThisFrame = False
        self._bottomArrowPressedTime = 0
        self._bottomArrowNumber = 0
        self._controlPressed = False
        self._cursorFlashingTime = 0.5
        self._cursorIsVisible = True
        self._cursorVisibleTime = 0
        self._leftArrowPressed = False
        self._leftArrowPressedTime = 0
        self._leftArrowNumber = 0
        self._returnPressed = False
        self._returnPressedTime = 0
        self._returnNumber = 0
        self._rightArrowPressed = False
        self._rightArrowPressedTime = 0
        self._rightArrowNumber = 0
        self._topArrowPressed = False
        self._topArrowPressedAtThisFrame = False
        self._topArrowPressedTime = 0
        self._topArrowNumber = 0

    def appendText(self, text, appendAtCursor = True, moveCursor = True): #Append "text" to text
        i = 0
        while i < len(text): #Delete ord(13) weird caracter
            if(ord(text[i])) == 13:
               text = text[:i] + text[i+1:len(text)]
               i -= 1
            i += 1
        
        newText = self.getText()
        if appendAtCursor:
            newText = newText[0:self.getCursorPosition()] + text + newText[self.getCursorPosition():]
        else:
            newText += text

        self.setText(newText)

        if moveCursor:
            self.setCursorPosition(self.getCursorPosition() + len(text))

    def getCursorPosition(self): #Return cursorPosition
        return self.cursorPosition
    
    def getCursorVisible(self): #Return cursorVisible
        return self.cursorVisible
    
    def getCursorWidth(self): #Return cursorWidth
        return self.cursorWidth
    
    def getCuttedText(self, generator):
        addLineToCursor = [] #Boolean list to see if the line is natural or not to the cursor
        pieces = []
        spaceWidth = generator.size(" ")[0]
        textWidth = self.getWidth() - (self.getFrameWidth(1) + self.getFrameWidth(3) + self.getTextOffset(1) + self.getTextOffset(3))

        if not self.getDynamicTextCut(): #Cut lines into pieces
            pieces = self.text.split("\n")
            for i in pieces:
                addLineToCursor.append(2)
        else:
            lines = self.text.split("\n")
            for line in lines:
                firstI = 0
                lastI = 0
                lineWidth = 0
                toAnalyze = line
                if self.dynamicTextCutType == 1:
                    toAnalyze = line.split(" ")

                for letter in toAnalyze: #Analyze caracter by caracter/word by word
                    letterSize = generator.size(letter)
                    if lineWidth + letterSize[0] > textWidth and firstI != lastI: #If words are bigger than one line
                        toAdd = ""
                        for i in range(firstI, lastI):
                            toAdd += toAnalyze[i]
                            if self.dynamicTextCutType == 1 and i != lastI - 1:
                                toAdd += " "
                        if self.getDynamicTextCutType() == 0:
                            addLineToCursor.append(0) #Cut by a caracter
                        else:
                            addLineToCursor.append(1) #Cut by a space
                        pieces.append(toAdd)
                        firstI = lastI
                        lineWidth = 0
                    lastI += 1
                    lineWidth += letterSize[0]
                    if self.dynamicTextCutType == 1:
                        lineWidth += spaceWidth

                if firstI < len(toAnalyze): #If last word/caracter didn't get analyzed
                    toAdd = ""
                    for i in range(firstI, len(toAnalyze)):
                        toAdd += toAnalyze[i]
                        if self.dynamicTextCutType == 1 and i != len(toAnalyze) - 1:
                            toAdd += " "
                    pieces.append(toAdd)

                if len(toAnalyze) == 0:
                    pieces.append("")

                addLineToCursor.append(2) #Cut by a line breaker

        return pieces.copy(), addLineToCursor.copy()

    def getDynamicTextCut(self): #Return dynamicTextCut
        return self.dynamicTextCut
    
    def getDynamicTextCutType(self): #Return dynamicTextCutType
        return self.dynamicTextCutType

    def getFont(self): #Return font
        return self.font
    
    def getFontSize(self): #Return fontSize
        return self.fontSize
    
    def getInput(self): #Return input
        return self.input

    def getSelectedText(self): #Return the selected text into the mtext
        if self.getSelection() and self.getSelectionStart() != self.getSelectionStop():
            return self.getText()[self.getSelectionStart():self.getSelectionStop()]
        else:
            return -1

    def getSelection(self): #Return selection
        return self.selection

    def getSelectionBackgroundColor(self): #Return selectionBackgroundColor
        return self.selectionBackgroundColor

    def getSelectionStart(self): #Return selectionStart
        return self.selectionStart
    
    def getSelectionStop(self): #Return selectionStart
        return self.selectionStop

    def getSelectionTextColor(self): #Return selectionTextColor
        return self.selectionTextColor

    def getText(self): #Return text
        return self.text
    
    def getTextColor(self): #Return textColor
        return self.textColor
    
    def getTextHorizontalAlignment(self): #Return textHorizontalAlignment
        return self.textHorizontalAlignment
    
    def getTextOffset(self, index): #Return textTopOffset if index = 0, textLeftOffset if index = 1, textBottomOffset if index = 2, textRightOffset if index = 3
        if index == 0:
            return self.textTopOffset
        elif index == 1:
            return self.textLeftOffset
        elif index == 2:
            return self.textBottomOffset
        else:
            return self.textRightOffset
    
    def getTextVerticalAlignment(self): #Return textVerticalAlignment
        return self.textVerticalAlignment
    
    def setCursorPosition(self, cursorPosition): #Change the value of cursorPosition
        if self.cursorPosition != cursorPosition and cursorPosition >= 0 and cursorPosition <= len(self.getText()):
            self.cursorPosition = cursorPosition
            self.setShouldModify(True)
    
    def setCursorVisible(self, cursorVisible): #Change the value of cursorVisible
        if self.cursorVisible != cursorVisible:
            self.cursorVisible = cursorVisible
            self.setShouldModify(True)

    def setCursorWidth(self, cursorWidth): #Change the value of cursorWidth
        if self.cursorWidth != cursorWidth:
            self.cursorWidth = cursorWidth
            if self.getCursorVisible() and self._getCursorIsVisible():
                self.setShouldModify(True)
    
    def setDynamicTextCut(self, dynamicTextCut): #Change the value of dynamicTextCut
        if self.dynamicTextCut != dynamicTextCut:
            self.dynamicTextCut = dynamicTextCut
            self.setShouldModify(True)

    def setDynamicTextCutType(self, dynamicTextCutType): #Change the value of dynamicTextCutType
        if self.dynamicTextCutType != dynamicTextCutType:
            self.dynamicTextCutType = dynamicTextCutType
            self.setShouldModify(True)
    
    def setFont(self, font): #Change the value of font
        if self.font != font:
            self.font = font
            self.setShouldModify(True)
    
    def setFontSize(self, fontSize): #Change the value of fontSize
        if self.fontSize != fontSize:
            self.fontSize = fontSize
            self.setShouldModify(True)

    def setInput(self, input): #Change the value of input
        self.input = input
        self.setCursorVisible(input)
        self.setSelection(input)
    
    def setSelection(self, selection): #Change the value of selection
        if selection != self.getSelection():
            self.selection = selection
            if self.selectionStart != self.selectionStop:
                self.setShouldModify(True)

    def setSelectionBackgroundColor(self, selectionBackgroundColor): #Change the value of selectionBackgroundColor
        if selectionBackgroundColor != self.getSelectionBackgroundColor():
            self.selectionBackgroundColor = selectionBackgroundColor
            if self.getSelection() and self.getSelectionStart() != self.getSelectionStop():
                self.setShouldModify(True)

    def setSelectionPos(self, selectionStart, selectionStop): #Change the value of selectionStart and selectionStop more easily
        self.setSelectionStop(len(self.getText()) + 1) #Neutralize _checkSelection effect
        self.setSelectionStart(0)
        self.setSelectionStop(selectionStop) #Apply modifications
        self.setSelectionStart(selectionStart)

    def setSelectionStart(self, selectionStart): #Change the value of selectionStart
        if selectionStart != self.getSelectionStart():
            self.selectionStart = selectionStart
            if self.selectionStart < 0:
                self.selectionStart = 0
            if self.getSelectionStart() > self.getSelectionStop():
                s = self.getSelectionStart()
                self.setSelectionStart(self.getSelectionStop())
                self.setSelectionStop(s)
            else:
                if self.getSelection():
                    self.setShouldModify(True)

    def setSelectionStop(self, selectionStop): #Change the value of selectionStop
        if selectionStop != self.getSelectionStop():
            self.selectionStop = selectionStop
            if self.getSelectionStop() > len(self.getText()) + 1:
                self.setSelectionStop(len(self.getText()) + 1)
            if self.getSelectionStop() < self.getSelectionStart():
                s = self.getSelectionStart()
                self.setSelectionStart(self.getSelectionStop())
                self.setSelectionStop(s)
            else:
                if self.getSelection():
                    self.setShouldModify(True)

    def setSelectionTextColor(self, selectionTextColor): #Change the value of selectionTextColor
        if selectionTextColor != self.getSelectionTextColor():
            self.selectionTextColor = selectionTextColor
            if self.getSelection() and self.getSelectionStart() != self.getSelectionStop():
                self.setShouldModify(True)

    def setText(self, text): #Change the value of text
        if self.text != text:
            self.text = text
            self._checkSelection()
            self._cursorVisibleTime = 0
            self._setCursorIsVisible(True)
            self.setShouldModify(True)

    def setTextColor(self, textColor): #Change the value of textColor
        if self.textColor != textColor:
            self.textColor = textColor
            self.setShouldModify(True)

    def setTextHorizontalAlignment(self, textHorizonAlignment): #Change the value of textAlignment
        if self.textHorizontalAlignment != textHorizonAlignment:
            self.textHorizontalAlignment = textHorizonAlignment
            self.setShouldModify(True)

    def setTextOffset(self, textOffset, index = -1): #Change the value of textTopOffset if index = 0, textLeftOffset if index = 1, textBottomOffset if index = 2, textRightOffset if index = 3
        if index == 0 and self.textTopOffset != textOffset:
            self.textTopOffset = textOffset
            self.setShouldModify(True)
        elif index == 1 and self.textLeftOffset != textOffset:
            self.textLeftOffset = textOffset
            self.setShouldModify(True)
        elif index == 2 and self.textBottomOffset != textOffset:
            self.textBottomOffset = textOffset
            self.setShouldModify(True)
        elif index == 3 and self.textRightOffset != textOffset:
            self.textRightOffset = textOffset
            self.setShouldModify(True)
        elif not (self.textTopOffset != textOffset and self.textLeftOffset == textOffset and self.textBottomOffset == textOffset and self.textRightOffset == textOffset):
            self.textTopOffset = textOffset
            self.textLeftOffset = textOffset
            self.textBottomOffset = textOffset
            self.textRightOffset = textOffset
            self.setShouldModify(True)

    def setTextVerticalAlignment(self, textVerticalAlignment): #Change the value of textAlignment
        if self.textVerticalAlignment != textVerticalAlignment:
            self.textVerticalAlignment = textVerticalAlignment
            self.setShouldModify(True)

    def _checkSelection(self): #Check if the selection is still good according to the text
        if self.selection:
            if self.getSelectionStart() < 0:
                self.setSelectionStart(0)
            if self.getSelectionStop() > len(self.getText()) + 1:
                self.setSelectionStop(len(self.getText()) + 1)
            if self.getSelectionStart() > self.getSelectionStop():
                s = self.getSelectionStart()
                self.setSelectionStart(self.getSelectionStop())
                self.setSelectionStop(s)

    def _cursorBottom(self): #Put up the cursor into the line at the top
        self._setCursorIsVisible(True)

        generator = pygame.font.SysFont(self.getFont(), self.getFontSize())
        heightCursor = generator.size(" ")[1]

        x = self._getPositionX(generator, self.getCursorPosition())
        y = self._getPositionY(generator, self.getCursorPosition()) + heightCursor + heightCursor/2

        pos = self._getPositionAtPos(generator, (x, y))

        self.setCursorPosition(pos)
        self.setSelectionPos(0, 0)
        self._baseSelection = 0

    def _cursorTop(self): #Put down the cursor into the line at the top
        self._setCursorIsVisible(True)

        generator = pygame.font.SysFont(self.getFont(), self.getFontSize())
        heightCursor = generator.size(" ")[1]

        x = self._getPositionX(generator, self.getCursorPosition())
        y = self._getPositionY(generator, self.getCursorPosition()) - heightCursor/2

        pos = self._getPositionAtPos(generator, (x, y))
        if y < 0:
            pos = 0

        self.setCursorPosition(pos)
        self.setSelectionPos(0, 0)
        self._baseSelection = 0
    
    def _doBackspaceEffet(self): #Do the effect of the pression fo the backspace touch
        if self.getInput():
            if self.getSelection() and self.getSelectedText() != -1:
                self._removeTextAtPos(len(self.getSelectedText()), self.getSelectionStop())
                self.setSelectionPos(0, 0)
            else:
                self._removeTextAtPos(1, self.getCursorPosition())

    def _getCursorIsVisible(self): #Return the value of _cursorIsVisible
        return self._cursorIsVisible
    
    def _getPositionLine(self, generator, position): #Return the line of the cursor
        pieces, piecesLineReturn = self.getCuttedText(generator)

        i = 0
        yCursor = 0
        textLength = 0
        for piece in pieces: #Analyze text line par line
            textLength += len(piece)

            offset = 0
            if piecesLineReturn[i] != 0:
                textLength += 1
            else:
                offset = 1

            if textLength <= position - offset:
                yCursor += 1
            else:
                return yCursor
            
            i += 1
        return yCursor

    def _getPositionAtPos(self, generator, pos): #Return the position of the cursor at one pos
        pieces = self.getCuttedText(generator)
        
        i = 0
        lineLength = 0
        textLength = 0
        x = self.getFrameWidth(1) + self.getTextOffset(1)
        y = self.getFrameWidth(0) + self.getTextOffset(0)

        if self.getTextVerticalAlignment() == 1:
            y = self.getFrameWidth(0) + self.getTextOffset(0)
            y += (((self.getHeight()-(self.getFrameWidth(0)+self.getFrameWidth(2)+self.getTextOffset(0)+self.getTextOffset(2)))/2) - self._getTextHeight(generator)/2)
        elif self.getTextVerticalAlignment() == 2:
            y = self.getHeight() - (self.getFrameWidth(2) + self._getTextHeight(generator) + self.getTextOffset(2))

        if pos[1] < y:
            return 0

        for piece in pieces[0]: #Search for y
            size = generator.size(piece)

            lineLength = size[0]
            y += size[1]
            if y > pos[1]:
                break
            else:
                textLength += len(piece)

            if pieces[1][i] != 0:
                textLength += 1

            i += 1

        if i == len(pieces[0]):
            i -= 1

        if self.getTextHorizontalAlignment() == 1:
            x = self.getTextOffset(1) + ((self.getWidth()-(self.getTextOffset(1)+self.getTextOffset(3)))/2) - lineLength/2
        elif self.getTextHorizontalAlignment() == 2:
            x = self.getWidth() - (self.getFrameWidth(3) + lineLength + self.getTextOffset(3))

        for piece in pieces[0][i]: #Search for x
            textLength += 1
            toAdd = generator.size(piece)[0]
            x += toAdd
            if x > pos[0]:
                if (x - pos[0]) > (pos[0] - (x - toAdd)):
                    textLength -= 1
                break

        return textLength

    def _getPositionX(self, generator, position): #Return the x pos of the cursor
        pieces, piecesLineReturn = self.getCuttedText(generator)

        i = -1
        lineSize = 0
        textLength = 0
        textSize = -1
        for piece in pieces: #Analyze each lines
            i += 1

            textLength += len(piece)
            if textLength >= position:
                lineSize = generator.size(piece)[0]
                textSize = generator.size(piece[0:(position-(textLength-len(piece)))])[0]
                break

            if piecesLineReturn[i] != 0:
                textLength += 1

        if textSize == -1:
            lineSize = generator.size(pieces[-1])[0]
            textSize = lineSize

        #return textSize
        if self.getTextHorizontalAlignment() == 0: #Apply alignment modification
            return textSize + self.getFrameWidth(1) + self.getTextOffset(1)
        elif self.getTextHorizontalAlignment() == 1:
            return self.getTextOffset(1) + ((self.getWidth()-(self.getTextOffset(1)+self.getTextOffset(3)))/2-lineSize/2) + textSize
        else:
            return self.getWidth() - (self.getFrameWidth(3) + (lineSize - textSize) + self.getTextOffset(3))
    
    def _getPositionY(self, generator, position): #Return the y pos of the cursor
        surfaces = self._getTextRendered(generator)

        i = 0
        line = self._getPositionLine(generator, position)
        textHeight = 0
        yAssignee = True
        yCursor = -1
        for piece in surfaces: #Analyze each lines
            textHeight += piece.get_height()

            if i >= line and yAssignee:
                yAssignee = False
                yCursor = textHeight - piece.get_height()
                
            i += 1

        if yCursor == -1:
            yCursor = textHeight - surfaces[-1].get_height()

        if self.getTextVerticalAlignment() == 0: #Apply alignment modification
            yCursor += self.getFrameWidth(0) + self.getTextOffset(0)
        elif self.getTextVerticalAlignment() == 1:
            yCursor += self.getFrameWidth(0) + self.getTextOffset(0) + ((self.getHeight()-(self.getFrameWidth(0)+self.getFrameWidth(2)+self.getTextOffset(0)+self.getTextOffset(2)))/2-textHeight/2)
        else:
            yCursor = (self.getHeight()-((textHeight-yCursor)+self.getFrameWidth(2)+self.getTextOffset(2)))

        return yCursor
    
    def _getTextHeight(self, generator): #Return the height of the text
        pieces = self.getCuttedText(generator)[0]
        textHeight = 0

        for piece in pieces:
            textHeight += generator.size(piece)[1]
        return textHeight
    
    def _getTextRendered(self, generator): #Return a list with all the text rendered
        pieces, addLineToReturn = self.getCuttedText(generator)
        
        i = 0
        isSelected = False
        selectionStarted = False
        selectionStartOffset = -1
        surfaces = []
        textLength = 0
        for piece in pieces: #Render text into pieces
            textLength += len(piece)
            if addLineToReturn[i] != 0:
                textLength += 1
            if self.getSelection() and self.getSelectionStart() != self.getSelectionStop() and textLength > self.getSelectionStart() + selectionStartOffset and (not selectionStarted or isSelected): #If the selection start at this line
                if not selectionStarted: #Start selection
                    isSelected = True
                    selectionStarted = True
                    if textLength > self.getSelectionStop() + selectionStartOffset: #And end at this line too
                        textSurface1 = generator.render(piece[:len(piece)-(textLength-self.getSelectionStart()+selectionStartOffset)], False, self.getTextColor())
                        textSurface2 = generator.render(piece[len(piece)-(textLength-self.getSelectionStart()+selectionStartOffset):len(piece)-(textLength-self.getSelectionStop()+selectionStartOffset)], False, self.getSelectionTextColor())
                        textSurface3 = generator.render(piece[len(piece)-(textLength-self.getSelectionStop()+selectionStartOffset):], False, self.getTextColor())
                        surfaceSelectionBackground = Surface((textSurface2.get_width(), textSurface2.get_height()), pygame.SRCALPHA)
                        surfaceSelectionBackground.fill(self.getSelectionBackgroundColor())
                        textSurface = Surface((textSurface1.get_width() + textSurface2.get_width() + textSurface3.get_width(), textSurface2.get_height()), pygame.SRCALPHA)
                        textSurface.blit(surfaceSelectionBackground, (textSurface1.get_width(), 0, textSurface2.get_width(), textSurface2.get_height()))
                        textSurface.blit(textSurface1, (0, 0, textSurface1.get_width(), textSurface1.get_height()))
                        textSurface.blit(textSurface2, (textSurface1.get_width(), 0, textSurface2.get_width(), textSurface2.get_height()))
                        textSurface.blit(textSurface3, (textSurface1.get_width() + textSurface2.get_width(), 0, textSurface3.get_width(), textSurface3.get_height()))
                        surfaces.append(textSurface)
                        isSelected = False
                    else:
                        textSurface1 = generator.render(piece[:len(piece)-(textLength-self.getSelectionStart()+selectionStartOffset)], False, self.getTextColor())
                        textSurface2 = generator.render(piece[len(piece)-(textLength-self.getSelectionStart()+selectionStartOffset):len(piece)-(textLength-self.getSelectionStop())], False, self.getSelectionTextColor())
                        surfaceSelectionBackground = Surface((textSurface2.get_width(), textSurface2.get_height()), pygame.SRCALPHA)
                        surfaceSelectionBackground.fill(self.getSelectionBackgroundColor())
                        textSurface = Surface((textSurface1.get_width() + textSurface2.get_width(), textSurface2.get_height()), pygame.SRCALPHA)
                        textSurface.blit(surfaceSelectionBackground, (textSurface1.get_width(), 0, textSurface2.get_width(), textSurface2.get_height()))
                        textSurface.blit(textSurface1, (0, 0, textSurface1.get_width(), textSurface1.get_height()))
                        textSurface.blit(textSurface2, (textSurface1.get_width(), 0, textSurface2.get_width(), textSurface2.get_height()))
                        surfaces.append(textSurface)
                elif isSelected: #Line in the middle of the selection
                    if textLength <= self.getSelectionStop() + selectionStartOffset: #And end at this line too
                        textSurface1 = generator.render(piece, False, self.getSelectionTextColor())
                        surfaceSelectionBackground = Surface((textSurface1.get_width(), textSurface1.get_height()), pygame.SRCALPHA)
                        surfaceSelectionBackground.fill(self.getSelectionBackgroundColor())
                        textSurface = Surface((textSurface1.get_width() + textSurface1.get_width(), textSurface1.get_height()), pygame.SRCALPHA)
                        textSurface.blit(surfaceSelectionBackground, (0, 0, textSurface1.get_width(), textSurface1.get_height()))
                        textSurface.blit(textSurface1, (0, 0, textSurface1.get_width(), textSurface1.get_height()))
                        surfaces.append(textSurface)
                    else: #End selection in a another line than the first selection position
                        textSurface1 = generator.render(piece[:len(piece)-(textLength-self.getSelectionStop() + selectionStartOffset)], False, self.getSelectionTextColor())
                        textSurface2 = generator.render(piece[len(piece)-(textLength-self.getSelectionStop() + selectionStartOffset):], False, self.getTextColor())
                        surfaceSelectionBackground = Surface((textSurface1.get_width(), textSurface1.get_height()), pygame.SRCALPHA)
                        surfaceSelectionBackground.fill(self.getSelectionBackgroundColor())
                        textSurface = Surface((textSurface1.get_width() + textSurface2.get_width(), textSurface2.get_height()), pygame.SRCALPHA)
                        textSurface.blit(surfaceSelectionBackground, (0, 0, textSurface1.get_width(), textSurface1.get_height()))
                        textSurface.blit(textSurface1, (0, 0, textSurface1.get_width(), textSurface1.get_height()))
                        textSurface.blit(textSurface2, (textSurface1.get_width(), 0, textSurface2.get_width(), textSurface2.get_height()))
                        surfaces.append(textSurface)
                        isSelected = False
            else:
                textSurface = generator.render(piece, False, self.textColor)
                surfaces.append(textSurface)
            i += 1
        
        return surfaces
    
    def _isGettingMouseDown(self, button, relativePos): #Function usefull for heritage, call by MApp when the widget is clicked by the mouse
        if button == 1:
            cursorPos = self._getPositionAtPos(pygame.font.SysFont(self.font, self.fontSize), relativePos)
            if self.getCursorVisible():
                self._cursorIsVisible = True
                self._cursorVisibleTime = 0
                self.setCursorPosition(cursorPos)
                self.setShouldModify(True)
            self.setSelectionPos(cursorPos, cursorPos)
            self._baseSelection = cursorPos

    def _isGettingMouseUp(self, button, relativePos): ##Function usefull for heritage, call by MApp when the widget isn't clicked by the mouse anymore
        if button == 1:
            cursorPos = self._getPositionAtPos(pygame.font.SysFont(self.font, self.fontSize), relativePos)
            if self.getCursorVisible():
                self.setCursorPosition(cursorPos)
                
    def _isKeyGettingDropped(self, key): #Function usefull for heritage, call by MApp when the widget is focused and a key is dropped on the keyboard (applicated for only one frame)
        if key == pygame.K_DOWN:
            self._bottomArrowPressed = False
            self._bottomArrowPressedTime = 0
            self._bottomArrowNumber = 0
        elif key == pygame.K_LEFT:
            self._leftArrowPressed = False
            self._leftArrowPressedTime = 0
            self._leftArrowNumber = 0
        elif key == pygame.K_RIGHT:
            self._rightArrowPressed = False
            self._rightArrowPressedTime = 0
            self._rightArrowNumber = 0
        elif key == pygame.K_UP:
            self._topArrowPressed = False
            self._topArrowPressedTime = 0
            self._topArrowNumber = 0
        
        if key == pygame.K_BACKSPACE:
            self._backspacePressed = False
            self._backspacePressedTime = 0
            self._backspaceNumber = 0
        elif key == pygame.K_RCTRL or key == pygame.K_LCTRL:
            self._controlPressed = False
        elif key == pygame.K_RETURN:
            self._returnPressed = False
            self._returnPressedTime = 0
            self._returnNumber = 0

    def _isKeyGettingPressed(self, key): #Function usefull for heritage, call by MApp when the widget is focused and a key is pressed on the keyboard (applicated for only one frame)
        if self.getCursorVisible(): #Cursor navigation
            if key == pygame.K_DOWN:
                self._cursorBottom()
                self._bottomArrowPressedAtThisFrame = True
                self.setShouldModify(True)

                self._bottomArrowPressed = True
                self._bottomArrowPressedTime = 0
                self._bottomArrowNumber = 0
            elif key == pygame.K_LEFT and len(self.getText()) > 0:
                self.setCursorPosition(self.getCursorPosition() - 1)
                self.setSelectionPos(0, 0)
                self._baseSelection = 0
                self._cursorVisibleTime = 0
                self._setCursorIsVisible(True)

                self._leftArrowPressed = True
                self._leftArrowPressedTime = 0
                self._leftArrowNumber = 0
            elif key == pygame.K_RIGHT and len(self.getText()) > 0:
                self.setCursorPosition(self.getCursorPosition() + 1)
                self.setSelectionPos(0, 0)
                self._baseSelection = 0
                self._cursorVisibleTime = 0
                self._setCursorIsVisible(True)

                self._rightArrowPressed = True
                self._rightArrowPressedTime = 0
                self._rightArrowNumber = 0
            elif key == pygame.K_UP:
                self._cursorTop()
                self._topArrowPressedAtThisFrame = True
                self.setShouldModify(True)

                self._topArrowPressed = True
                self._topArrowPressedTime = 0
                self._topArrowNumber = 0
        
        if self.getInput(): #Special touch handle
            if key == pygame.K_BACKSPACE:
                self._doBackspaceEffet()
                self._backspacePressed = True
                self._backspacePressedTime = 0
                self._backspaceNumber = 0
            elif key == pygame.K_RCTRL or key == pygame.K_LCTRL:
                self._controlPressed = True
            elif key == pygame.K_RETURN:
                if self.getSelection() and self.getSelectedText() != -1:
                    self._removeTextAtPos(len(self.getSelectedText()), self.getSelectionStop())
                    self.setSelectionPos(0, 0)
                self.appendText("\n")
                self._returnPressed = True
                self._returnPressedTime = 0
                self._returnNumber = 0
            elif key == pygame.K_a and self._controlPressed:
                self.setCursorPosition(len(self.getText()))
                self.setSelectionPos(0, len(self.getText()))
            elif key == pygame.K_c and self._controlPressed:
                if self.getSelection() and self.getSelectedText() != -1:
                    copy(self.getSelectedText())
            elif key == pygame.K_v and self._controlPressed:
                if self.getSelection() and self.getSelectedText() != -1:
                    self._removeTextAtPos(len(self.getSelectedText()), self.getSelectionStop())
                    self.setSelectionPos(0, 0)
                self.appendText(paste())
            elif key == pygame.K_x and self._controlPressed:
                if self.getSelection() and self.getSelectedText() != -1:
                    copy(self.getSelectedText())
                    self._removeTextAtPos(len(self.getSelectedText()), self.getSelectionStop())
                    self.setSelectionPos(0, 0)

    def _isNotFocusedAnymore(self): #Function usefull for heritage, call by MApp when the widget is not focused anymore
        self._bottomArrowPressed = False
        self._bottomArrowPressedTime = 0
        self._bottomArrowNumber = 0
        self._backspacePressed = False
        self._backspacePressedTime = 0
        self._backspaceNumber = 0
        self._controlPressed = False
        self._leftArrowPressed = False
        self._leftArrowPressedTime = 0
        self._leftArrowNumber = 0
        self._returnPressed = False
        self._returnPressedTime = 0
        self._returnNumber = 0
        self._rightArrowPressed = False
        self._rightArrowPressedTime = 0
        self._rightArrowNumber = 0
        self._topArrowPressed = False
        self._topArrowPressedTime = 0
        self._topArrowNumber = 0
        
        self.setSelectionPos(0, 0)

        if self.getCursorVisible() or self.getSelection():
            self.setShouldModify(True)

    def _isTextGettingEntered(self, text): #Function usefull for heritage, call by MApp when the widget is focused and the user is entering a text (applicated for only one frame)
        if self.getInput():
            if self.getSelection() and self.getSelectedText() != -1:
                self._removeTextAtPos(len(self.getSelectedText()), self.getSelectionStop())
                self.setSelectionPos(0, 0)
            self.appendText(text)

    def _mouseMove(self, buttons, pos, relativeMove): #Function usefull for heritage, call by MApp when the widget is focused and the mouse is moving
        if buttons.count(1) > 0:
            if self.getCursorVisible() or self.getSelection():
                cursorPos = self._getPositionAtPos(pygame.font.SysFont(self.font, self.fontSize), pos)
                if self.getCursorVisible():
                    self.setCursorPosition(cursorPos)
                if self.getSelection():
                    if cursorPos >= self.getSelectionStop():
                        self.setSelectionPos(self._baseSelection, cursorPos)
                    else:
                        self.setSelectionPos(cursorPos, self._baseSelection)

    def _removeTextAtPos(self, length, pos): #Remove a length-sized piece of text at the cursor
        firstI = pos - length
        if firstI <= -1:
            firstI = 0
        if self.getCursorPosition() >= pos:
            self.setCursorPosition(self.getCursorPosition() - length)
        elif self.getCursorPosition() >= pos - length:
            self.setCursorPosition(pos - length)
        self.setText(self.getText()[:firstI] + self.getText()[pos:])

    def _renderBeforeHierarchy(self, surface): #Render widget on surface before hierarchy render
        surface = super()._renderBeforeHierarchy(surface)

        generator = pygame.font.SysFont(self.font, self.fontSize)
        heightCursor = generator.size(" ")[1]
        x = self.getFrameWidth(1) + self.getTextOffset(1)
        y = self.getFrameWidth(0) + self.getTextOffset(0)

        if self.getTextVerticalAlignment() == 2:
            y = self.getHeight() - (self.getFrameWidth(2) + self.getTextOffset(2))

        surfaces = self._getTextRendered(generator) #Get the text rendered into surface
        textHeight = 0
        for textSurface in surfaces:
            textHeight += textSurface.get_height()

        if self.getTextVerticalAlignment() == 1: #Calculate y including vertical alignment particularity
            y = self.getFrameWidth(0) + self.getTextOffset(0) + ((self.getHeight()-(self.getFrameWidth(0)+self.getFrameWidth(2)+self.getTextOffset(0)+self.getTextOffset(2)))/2 - textHeight/2)

        if self.getTextVerticalAlignment() == 2:
            surfaces = surfaces[::-1]

        for textSurface in surfaces: #Place text
            if self.getTextHorizontalAlignment() == 1:
                x = self.getTextOffset(1) + ((self.getWidth()-(self.getFrameWidth(1)+self.getFrameWidth(3)+self.getTextOffset(1)+self.getTextOffset(3)))/2) - textSurface.get_width()/2
            elif self.getTextHorizontalAlignment() == 2:
                x = self.getWidth() - (self.getFrameWidth(3) + textSurface.get_width() + self.getTextOffset(3))

            if self.getTextVerticalAlignment() == 2:
                y -= textSurface.get_height()

            surface.blit(textSurface, (x, y, textSurface.get_width(), textSurface.get_height()))
            
            if self.getTextVerticalAlignment() != 2:
                y += textSurface.get_height()

        if self.getCursorVisible() and self._getCursorIsVisible() and self.getFocused(): #Draw cursor
            xCursor = self._getPositionX(generator, self.getCursorPosition())
            yCursor = self._getPositionY(generator, self.getCursorPosition())
            pygame.draw.rect(surface, (0, 0, 0), (xCursor, yCursor, self.getCursorWidth(), heightCursor))

        return surface
    
    def _setCursorIsVisible(self, _cursorIsVisible): #Change the value of _cursorIsVisible
        if self._cursorIsVisible != _cursorIsVisible:
            self._cursorIsVisible = _cursorIsVisible
            self.setShouldModify(True)
    
    def _update(self, deltaTime):

        if self._backspacePressed:
            self._backspacePressedTime += deltaTime
            if self._backspacePressedTime > 0.5:
                n = (self._backspacePressedTime - 0.5)*10
                if ceil(n) >= self._backspaceNumber:
                    self._doBackspaceEffet()
                    self._backspaceNumber += 0.5

        if self._bottomArrowPressed:
            self._bottomArrowPressedTime += deltaTime
            if self._bottomArrowPressedTime > 0.5:
                n = (self._bottomArrowPressedTime - 0.5)*10
                if ceil(n) >= self._bottomArrowNumber:
                    self._bottomArrowPressedAtThisFrame = True
                    self._bottomArrowNumber += 0.5
                    self._cursorBottom()

        if self._leftArrowPressed:
            self._leftArrowPressedTime += deltaTime
            if self._leftArrowPressedTime > 0.5:
                n = (self._leftArrowPressedTime - 0.5)*10
                if ceil(n) >= self._leftArrowNumber:
                    self.setCursorPosition(self.getCursorPosition() - 1)
                    self._cursorVisibleTime = 0
                    self._setCursorIsVisible(True)
                    self._leftArrowNumber += 0.5

        if self._returnPressed:
            self._returnPressedTime += deltaTime
            if self._returnPressedTime > 0.5:
                n = (self._returnPressedTime - 0.5)*10
                if ceil(n) >= self._returnNumber:
                    if self.getSelection() and self.getSelectedText() != -1:
                        self._removeTextAtPos(len(self.getSelectedText()), self.getSelectionStop())
                        self.setSelectionPos(0, 0)
                    self.appendText("\n")
                    self._returnNumber += 0.5

        if self._rightArrowPressed:
            self._rightArrowPressedTime += deltaTime
            if self._rightArrowPressedTime > 0.5:
                n = (self._rightArrowPressedTime - 0.5)*10
                if ceil(n) >= self._rightArrowNumber:
                    self.setCursorPosition(self.getCursorPosition() + 1)
                    self._cursorVisibleTime = 0
                    self._setCursorIsVisible(True)
                    self._rightArrowNumber += 0.5

        if self._topArrowPressed:
            self._topArrowPressedTime += deltaTime
            if self._topArrowPressedTime > 0.5:
                n = (self._topArrowPressedTime - 0.5)*10
                if ceil(n) >= self._topArrowNumber:
                    self._topArrowPressedAtThisFrame = True
                    self._topArrowNumber += 0.5
                    self._cursorTop()

        if self.getCursorVisible() and self.getFocused():
            self._cursorVisibleTime += deltaTime
            if self._cursorVisibleTime >= self._cursorFlashingTime:
                self._cursorVisibleTime -= self._cursorFlashingTime
                self._setCursorIsVisible(not self._cursorIsVisible)