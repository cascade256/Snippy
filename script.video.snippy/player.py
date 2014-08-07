import xbmc

class MyPlayer(xbmc.Player):
    def onPlayBackStarted(self):
        global onPlayBackStartedCallback
        onPlayBackStartedCallback()
def play():
    if(xbmc.getCondVisibility("Player.Paused") == 1):
        print "Snippy: play"
        player.pause()
    else:
        print "Snippy: play, but not paused"
def pause():
    if(xbmc.getCondVisibility("Player.Paused") == 0):
        print "Snippy: pause"
        player.pause()
    else:
        print "Snippy: pause, but not playing"
def getTime():
    return player.getTime()
def jumpForwardShort():
    player.seekTime(player.getTime() + 15)
def jumpBackShort():
    player.seekTime(player.getTime() - 15)
def jumpForwardLong():
    player.seekTime(player.getTime() + 300)
def jumpBackLong():
    player.seekTime(player.getTime() - 300)
def onPlayBackStarted(callback):
    global onPlayBackStartedCallback
    onPlayBackStartedCallback = callback

def init():
    global player
    player = MyPlayer()
player = None
onPlayBackStartedCallback = None