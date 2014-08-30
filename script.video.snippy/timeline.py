import xbmcgui, xbmcaddon
import os

tWindow = None
lines = []
imagePath = None
cutColor = None
muteColor = None
commSkipColor = None
sceneMarkerColor = None
playColor = None
totalTime = None


def init(tWin, tTime):
    global tWindow, lines, imagePath, cutColor, muteColor, commSkipColor, sceneMarkerColor, playColor, totalTime
    
    tWindow = tWin
    
    cutColor = "0xFFFF0000" #red
    muteColor = "0xFFFF9D00" #orange
    commSkipColor = "0xFFFFFB00" #yellow
    sceneMarkerColor = "0xFF00FFFB" #light blue
    playColor = "0xFF00FF04" #green
    
    totalTime = tTime
    
    addonPath = xbmcaddon.Addon().getAddonInfo('path')
    imagePath = os.path.join(addonPath, "line.png")
    
    lines.append(xbmcgui.ControlImage(x=0,y=640, width=1280, height=10, filename=imagePath, colorDiffuse=playColor))
    tWindow.addControl(lines[0])
    
def refresh(edits):
    if len(edits) == 0:
        return
    global tWindow, lines, imagePath, cutColor, muteColor, commSkipColor, sceneMarkerColor, playColor, totalTime
    
    for line in lines:
        tWindow.removeControl(line)
    
    lines = []
        
    time = 0
    for edit in edits:
        createPlayLine(time, edit.startTime)
        createEditLine(edit)
        time = edit.endTime
        
    createPlayLine(time, totalTime)
    
    for line in lines:
        tWindow.addControl(line)
        
def createEditLine(edit):
    global tWindow, lines, imagePath, cutColor, muteColor, commSkipColor, sceneMarkerColor, playColor
    start = edit.startTime
    end = edit.endTime
    length = end - start
    color = None

    #edit types:
    #0 - Cut
    #1 - Mute
    #2 - Scene Marker
    #3 - Commercial Break
    if edit.type == 0:
        color = cutColor
    elif edit.type == 1:
        color = muteColor
    elif edit.type == 2:
        color = sceneMarkerColor
    elif edit.type == 3:
        color = commSkipColor
    else:
        print "Snippy: unknown edit type in timeline.refresh"
        
    lines.append(xbmcgui.ControlImage(x=timeToPixels(start), y=640, width=timeToPixels(length), height= 10, filename=imagePath,                         colorDiffuse=color))
def createPlayLine(startTime, endTime):
    global tWindow, lines, imagePath, playColor
                 
    start = startTime
    end = endTime
    length = end - start

    lines.append(xbmcgui.ControlImage(x=timeToPixels(start), y=640, width=timeToPixels(length), height=10, filename=imagePath, colorDiffuse=playColor))
    
def timeToPixels(time):
    global totalTime
    return int((1280 / totalTime) * time)
    