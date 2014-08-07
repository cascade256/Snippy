import pyxbmct.addonwindow as gui

class InputBox(gui.AddonDialogWindow):
    callback = None
    editBox = None
    def exitPopUp(self):
        self.close()
        text = self.editBox.getText()
        self.callback(text)
    def showPopUp(self, callback):
        self.callback = callback
        self.doModal()
        
    def __init__(self, title=''):
        super(InputBox, self).__init__(title)
        self.setGeometry(350, 150, 2, 2)
       
        self.editBox = gui.Edit(label="hi")
        self.placeControl(self.editBox, 0, 0, columnspan=2)
        
        confirmBtn = gui.Button("Confirm")
        self.placeControl(confirmBtn, 1, 0)
        self.connect(confirmBtn, self.exitPopUp)
        
        cancelBtn = gui.Button("Cancel")
        self.placeControl(cancelBtn, 1, 1)
        self.connect(cancelBtn, self.close)
        
class MessageBox(gui.AddonDialogWindow):
    def exitPopUp(self):
        self.close()
    def __init__(self, title, message):
        super(MessageBox, self).__init__(title)
        self.setGeometry(350, 150, 2, 1)
       
        label = gui.Label(message)
        self.placeControl(label, 0, 0)
        
        confirmBtn = gui.Button("Ok")
        self.placeControl(confirmBtn, 1, 0)
        self.connect(confirmBtn, self.exitPopUp)