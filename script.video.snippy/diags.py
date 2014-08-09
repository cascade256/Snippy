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
       
        self.editBox = gui.Edit("")
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
        
        
class SelectEditTypeBox(gui.AddonDialogWindow):
    callback = None
    optionsList = None
    def exitPopUp(self):
        self.close()
        selected = self.optionsList.getSelectedPosition()
        self.callback(selected)
    def showPopUp(self, callback):
        self.callback = callback
        self.doModal()
    def __init__(self, title):
        super(SelectEditTypeBox, self).__init__(title)
        self.setGeometry(350, 150, 3, 2)
        
        self.optionsList = gui.List()
        self.placeControl(self.optionsList, 0, 0, 
            columnspan=2, rowspan=2)
        self.optionsList.addItem("Cut")
        self.optionsList.addItem("Mute")
        self.optionsList.addItem("Scene Marker")
        self.optionsList.addItem("Commercial Break")
        
        
        confirmBtn = gui.Button("Confirm")
        self.placeControl(confirmBtn, 2, 0)
        self.connect(confirmBtn, self.exitPopUp)
        
        cancelBtn = gui.Button("Cancel")
        self.placeControl(cancelBtn, 2, 1)
        self.connect(cancelBtn, self.close)
        