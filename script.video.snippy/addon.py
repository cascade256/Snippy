import pyxbmct.addonwindow as gui
import xbmc
import diags
import player

quit = False
edits = []
editing = False
startTime = 0
endTime = 0
#edit types:
    #0 - Cut
    #1 - Mute
    #2 - Scene Marker
    #3 - Commercial Break
editType = 0
def close():
    print "Snippy: exiting"
    global window
    window.close()
    global quit
    quit = True
def startEdit():
    print "Snippy: start edit"
    global editing
    editing = True
    global startTime
    startTime = player.getTime()
def endEdit():
    print "Snippy: end edit"
    global editing
    if(editing):
        editing = False
        global edits
        global startTime
        global endTime
        endTime = player.getTime()
        #this always lists the edit as a cut, ideally change to a pop-up
        edits.append(Edit(startTime, endTime, 0))
        #printEdits()
    else:
        print "Snippy: end edit, but was not editing"
def printEdits():
    global edits
    for edit in edits:
        print "!" + str(edit.startTime) + ", " + str(edit.endTime)
def saveEDL(location):
    print "Snippy: saving"
    try:
        f = open(location, "w+")
        global edits
        for edit in edits:
            f.write(str(edit.startTime) + ' ' + str(edit.endTime) + 
                ' ' + str(edit.type) + '\n')
    except Exception, e:
        global messagebox
        messagebox = diags.MessageBox("Error", "Was unable to save, check the path")
        messagebox.doModal()
        print "Snippy: There was a problem saving the edl"
def openSaveWindow():
    global input
    input.showPopUp(saveEDL)
def openMainWindow():
    global window
    window.doModal()
class Edit:
    def __init__(self, startTime, endTime, type):
        self.startTime = startTime
        self.endTime = endTime
        self.type = type
    def __str__(self):
        return str(self.startTime) + str(self.endTime) + str(type)
class MainWindow(gui.BlankDialogWindow):
    def exit():
        global quit
        quit = True
        self.close()
    def __init__(self):
        super(MainWindow, self).__init__()
        rows = 11
        columns = 10
        self.setGeometry(1280, 720, rows + 1, columns)
        
        exitBtn = gui.Button("exit")
        self.placeControl(exitBtn,rows,0)
        self.connect(exitBtn, close)
        
        #play controls
        backLongBtn = gui.Button("<5min")
        self.placeControl(backLongBtn, rows, 1)
        self.connect(backLongBtn, player.jumpBackLong)
        
        backShortBtn = gui.Button("<15sec")
        self.placeControl(backShortBtn, rows, 2)
        self.connect(backShortBtn, player.jumpBackShort)
        
        playBtn = gui.Button("play")
        self.placeControl(playBtn, rows, 3)
        self.connect(playBtn, player.play)
      
        pauseBtn = gui.Button("pause")
        self.placeControl(pauseBtn, rows, 4)
        self.connect(pauseBtn, player.pause)
        
        
        forwardShortBtn = gui.Button("15sec>")
        self.placeControl(forwardShortBtn, rows, 5)
        self.connect(forwardShortBtn, player.jumpForwardShort)
        
        forwardLongBtn = gui.Button("5min>")
        self.placeControl(forwardLongBtn, rows, 6)
        self.connect(forwardLongBtn, player.jumpForwardLong)
        
        
        
        #edit buttons
        startEditBtn = gui.Button("start Edit")
        self.placeControl(startEditBtn, rows, 7)
        self.connect(startEditBtn, startEdit)
        
        endEditBtn = gui.Button("end Edit")
        self.placeControl(endEditBtn, rows, 8)
        self.connect(endEditBtn, endEdit)
        
        saveEditBtn = gui.Button("save Edits")
        self.placeControl(saveEditBtn, rows, 9)
        self.connect(saveEditBtn, openSaveWindow)
        
class MyMonitor(xbmc.Monitor):
    def onAbortRequested():
        global quit
        quit = True

        
        
window = MainWindow()
input = diags.InputBox("Save")
messagebox = diags.MessageBox("", "")
player.onPlayBackStarted(openMainWindow)
player.init()
monitor = MyMonitor()
        
if __name__ == "__main__":
    while quit == False:
        print 'Snippy: running'
        xbmc.sleep(1000)
    print "Snippy: quitting"