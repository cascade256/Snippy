import pyxbmct.addonwindow as gui
import xbmc, xbmcgui, xbmcaddon
import diags
import player
import timeline

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
    global window, quit
    print "Snippy: exiting"
    window.close()
    quit = True
    
def startEdit():
    global editing, startTime
    print "Snippy: start edit"
    editing = True
    startTime = player.getTime()
    showNotification("Snippy", "Started edit", 1500)
    
def endEdit():
    global editing, endTime, selectType
    print "Snippy: end edit"
    if(editing):
        editing = False
        #save the end time of the edit before showing the popup for 
        #selecting the type of edit
        endTime = player.getTime()
        player.pause()
        selectType = diags.SelectEditTypeBox("")
        selectType.showPopUp(addEdit)
        refreshWindow()
    else:
        print "Snippy: end edit, but was not editing"
        
def addEdit(type):
    if(type > -1 and type < 4):
        global startTime, endTime, edits
        edits.append(Edit(startTime, endTime, type))
    else:
        print "Snippy: something went wrong selecting the type"
        
def printEdits():
    global edits
    for edit in edits:
        print "!" + str(edit.startTime) + ", " + str(edit.endTime)

def saveEDL(location):
    global edits, messagebox
    print "Snippy: saving"
    try:
        f = open(location, "w+")
        for edit in edits:
            f.write(str(edit.startTime) + ' ' + str(edit.endTime) + 
                ' ' + str(edit.type) + '\n')
    except Exception, e:
        messagebox = diags.MessageBox("Error", "Was unable to save, check the path")
        messagebox.doModal()
        print "Snippy: There was a problem saving the edl"
        
def openSaveWindow():
    global input
    input.showPopUp(saveEDL)
    
def openMainWindow():
    global window
    timeline.init(window, player.getTotalTime())
    window.doModal()
    
def refreshWindow():
    global window, edits
    window.close()
    timeline.refresh(edits)
    window.doModal()
    
def showNotification(title, message, time):
    xbmc.executebuiltin("Notification(%s, %s, %d)"%(title,message,time))
    
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
    #def onAction(self, action):
        #print action.getButtonCode()
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
    def onAbortRequested(self):
        global quit
        quit = True
        
window = MainWindow()
input = diags.InputBox("Save")
selectType = diags.SelectEditTypeBox("")
messagebox = diags.MessageBox("", "")
player.onPlayBackStarted(openMainWindow)
player.init()
monitor = MyMonitor()
        
if __name__ == "__main__":
    showNotification("Snippy", "Started ready for you to start your video", 4000)
    while quit == False:
        print 'Snippy: running'
        xbmc.sleep(2000)
    print "Snippy: quitting"