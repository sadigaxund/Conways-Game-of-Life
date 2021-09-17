'''
MIT License

Copyright (c) 2021 Sadig Akhund

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


from util.graphics import Renderer
import pygame_gui 
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')
settings = config['COMPONENTS']
colors = config['COLORS']
fetchInt = lambda key : int(settings[key])

G2D = Renderer((fetchInt('WINDOW_WIDTH'), fetchInt('WINDOW_HEIGHT')), 'Clock') 
manager = pygame_gui.UIManager(G2D.WINDOW_SIZE)
MARGIN = fetchInt('MARGIN')



class Disk:
    def __init__(self, G2D, bounds, index, color = None) -> None:
        self.bounds = bounds
        self.pos = (bounds.top, bounds.left)
        self.size = (bounds.width, bounds.height)
        self.G2D = G2D
        self.index = index
        self.color = G2D.PEN.GREEN if color == None else color
        pass
    def draw(self):
        self.G2D.PEN.drawRoundRect(G2D.Rect(self.bounds.left, self.bounds.top,
                                     self.bounds.width, self.bounds.height), 5, self.color, stroke = 0)
        pass

class Tower:
    DISK_AMOUNT = 0
    DISKS:Disk = []

    def __init__(self, G2D, bounds) -> None:
        self.rod_width = int(bounds.width * 0.06)
        self.rod_height = int(bounds.height*1.35)
        self.base_width = int(bounds.width)
        self.base_height = int(bounds.height* 0.17)
        self.disk_height = int(bounds.height * 0.15)
        self.bounds = bounds
        self.G2D = G2D

    def addDisk(self, index = None, size = None, color = None):
        self.DISK_AMOUNT = self.DISK_AMOUNT + 1
        index = self.DISK_AMOUNT if index == None else index + 1
        t =  (10 - index + 1) / 15

        w = self.base_width * t
        h = self.disk_height
        (w, h) = (w, h) if size == None else size

        x = self.bounds.left + (self.base_width - w) / 2
        y = self.bounds.bottom - self.base_height - self.disk_height * self.DISK_AMOUNT 
        
        color = self.G2D.PEN.colorOnRainbow(t * 3 / 2 + 0.1) if color == None else color
        self.DISKS.append(Disk(self.G2D, self.G2D.Rect(x, y, w, h), index, color))
        
        
    def pop(self):
        self.DISK_AMOUNT = self.DISK_AMOUNT - 1
        return self.DISKS.pop()

    def push(self, disk):
        self.addDisk(size = disk.size, color = disk.color)
        
        
    
    def draw(self):
        # Draw Rod
        self.G2D.PEN.drawRoundRect(G2D.Rect(self.bounds.left + (self.bounds.width - self.rod_width)/2 - 1, self.bounds.bottom - self.rod_height - self.base_height + 5,
                                    self.rod_width, self.rod_height), 2, "#FFFFFF", 0)
        # Draw Disks
        for disk in self.DISKS:
            disk.draw()
        # Draw Base
        self.G2D.PEN.drawRoundRect(G2D.Rect(self.bounds.left, self.bounds.bottom - self.base_height, self.bounds.width, self.base_height), 2, "#964B00", 0)

        pass

tower_size = (200, 100)

y = G2D.WINDOW_SIZE[1] / 2 - tower_size[1] / 2
xMid = G2D.WINDOW_SIZE[0] / 2 - tower_size[0] / 2
someMargin = 100



towers =    [  
                Tower(G2D, G2D.Rect(xMid - tower_size[0] - someMargin, y, tower_size[0], tower_size[1])), 
                Tower(G2D, G2D.Rect(xMid, y, tower_size[0], tower_size[1])), 
                Tower(G2D, G2D.Rect(xMid + tower_size[0] + someMargin, y, tower_size[0], tower_size[1]))
            ]

def initTowers(startAmount):
    for tower in towers:
        while tower.DISK_AMOUNT > 0:
            tower.pop()

    for i in range(0, startAmount):
        towers[0].addDisk(8 - (startAmount - i - 1))

initTowers(3)

# rod1 = Rod(G2D, (100, 100), ROD_LENGTH)
def draw(this):
    G2D.PEN.fillBackground(colors['BACKGROUND'])
    for tower in towers:
        tower.draw()

DRAGING = False

def handleTowerDragging(tower:Tower, pos):
    global DRAGING, offset_x, offset_y, mouse_x, mouse_y, diskToDrag
    for disk in tower.DISKS:
        if disk.bounds.collidepoint(pos):
            print(disk)
            DRAGING = True
            mouse_x, mouse_y = pos
            offset_x = disk.bounds.x - mouse_x
            offset_y = disk.bounds.y - mouse_y
            diskToDrag = disk
            break
def handleDiskDragging(pos):
    global DRAGING, offset_x, offset_y, mouse_x, mouse_y, diskToDrag
    if DRAGING:
        mouse_x, mouse_y = pos
        diskToDrag.x = mouse_x + offset_x
        diskToDrag.y = mouse_y + offset_y


def handleEvent(this, event):
    manager.process_events(event)
    if event.type == G2D.PYGAME_INSTANCE_.MOUSEBUTTONDOWN and event.button == 1:
        for tower in towers:
            if tower.bounds.collidepoint(event.pos):
                print(tower)
                handleTowerDragging(tower, event.pos)
                break
    if event.type == G2D.PYGAME_INSTANCE_.MOUSEBUTTONUP:
            global DRAGING
            if event.button == 1:            
                DRAGING = False
    if event.type == G2D.PYGAME_INSTANCE_.MOUSEMOTION:
        handleDiskDragging(event.pos)
        pass



def update(this):
    global CANVAS_BORDER, BOTTOM_MENU_BORDERS, bottom_panel
    manager.update(G2D.clock.get_time()/1000.0)
    G2D.WINDOW.blit(G2D.WINDOW, (0, 0))
    manager.draw_ui(G2D.WINDOW)
    pass

G2D.setEventLogic(handleEvent)
G2D.setDrawLogic(draw)
G2D.setUpdateLogic(update)
G2D.startLoop()