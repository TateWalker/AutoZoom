import sys
from os import path
import json
sys.path.insert(1, 'lib')
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import restoreSettings
import keyValidation
import makeCron

class Tab(QWidget):

    def __init__(self, dl='', dc='', ds=QTime(0,0), de=QTime(0,0), dd=[], *args, **kwargs):
        super(Tab, self).__init__(*args, **kwargs)
        self.default_link = dl
        self.default_class = dc
        self.default_start = ds
        self.default_end = de
        self.default_days = dd
        self.init_ui()
        self.setLayout(self.main_tab_layout)

    def init_ui(self):
        self.main_tab_layout = QVBoxLayout()
        self.name_class_layout = QHBoxLayout()
        self.link_time_layout = QHBoxLayout()
        self.days_layout = QGridLayout()
        self.days_layout.setHorizontalSpacing(10)
        self.name_class_layout.addWidget(QLabel('Enter a valid Zoom link below:'))
        self.name_class_layout.addSpacing(168)
        self.name_class_layout.addWidget(QLabel('Class name:'))
        self.class_name = QLineEdit(self.default_class)
        self.name_class_layout.addWidget(self.class_name)
        self.zoom_link = QLineEdit(self.default_link)
        self.link_time_layout.addWidget(self.zoom_link)
        self.start_time = QTimeEdit(self.default_start)
        self.start_time.setDisplayFormat('unicode')
        self.link_time_layout.addWidget(self.start_time)
        self.link_time_layout.addWidget(QLabel('-'))
        self.end_time = QTimeEdit(self.default_end)
        self.end_time.setDisplayFormat('unicode')
        self.link_time_layout.addWidget(self.end_time)
        self.addCheckBoxes()
        self.main_tab_layout.addLayout(self.name_class_layout)
        self.main_tab_layout.addLayout(self.link_time_layout)
        self.main_tab_layout.addLayout(self.days_layout)

    def addCheckBoxes(self):
        self.day_widgets = [None]*7
        days = ['  Sunday',' Monday','  Tuesday','  Wednesday','  Thursday',' Friday','  Saturday']
        for count,day in enumerate(days):
            self.day_widgets[count] = QCheckBox()
            try:
                if self.default_days[count] == 1:
                    self.day_widgets[count].setCheckState(2)
                else:
                    self.day_widgets[count].setCheckState(0)
            except:
                self.day_widgets[count].setCheckState(0)
            
            self.days_layout.addWidget(self.day_widgets[count],0,count,Qt.AlignCenter)
            self.days_layout.addWidget(QLabel(day),1,count,Qt.AlignCenter)

def getPath(filename):
        bundle_dir = getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__)))
        path_to_file = path.join(bundle_dir, filename)
        return path_to_file

class WarningDialog(QDialog):
    def __init__(self, message, *args, **kwargs):
        super(WarningDialog, self).__init__(*args, **kwargs)
        self.message = message
        self.init_ui()
        self.setLayout(self.layout1)
        self.exec()

    def init_ui(self):
        self.resize(600, 100)
        self.center()
        self.setWindowTitle("Oops!")
        self.layout1 = QVBoxLayout()
        self.layout2 = QHBoxLayout()
        self.confirmation = QPushButton('Ok', self)
        self.prompt = QLabel(self.message)
        self.prompt.setAlignment(Qt.AlignCenter)
        self.layout2.addSpacing(100)
        self.layout1.addWidget(self.prompt)
        self.layout1.addLayout(self.layout2)
        self.layout2.addWidget(self.confirmation)
        self.layout2.addSpacing(100)
        self.confirmation.clicked.connect(self.closeEvent)

    def closeEvent(self,event):
        self.hide()

    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

class ClearDialog(WarningDialog):

    def init_ui(self):
        self.resize(600, 100)
        self.center()
        self.setWindowTitle("Clear Classes")
        self.layout1 = QVBoxLayout()
        self.layout2 = QHBoxLayout()
        self.confirmation = QPushButton('Ok', self)
        self.cancel = QPushButton('Cancel', self)
        self.prompt = QLabel(self.message)
        self.prompt.setAlignment(Qt.AlignCenter)
        self.layout2.addSpacing(100)
        self.layout1.addWidget(self.prompt)
        self.layout1.addLayout(self.layout2)
        self.layout2.addWidget(self.confirmation)
        self.layout2.addWidget(self.cancel)
        self.layout2.addSpacing(100)
        self.cancel.clicked.connect(self.isCanceled)
        self.confirmation.clicked.connect(self.isNotCanceled)

    def isCanceled(self):
        self.canceled = True
        self.hide()

    def isNotCanceled(self):
        self.canceled = False
        self.hide()

class KeyWindow(QDialog):
    def __init__(self, *args, **kwargs):
        super(KeyWindow, self).__init__(*args, **kwargs)
        # self.setWindowModality(Qt.ApplicationModal)
        keyFile = getPath('.keyFile')
        self.key = ''
        try:
            with open(keyFile,'r') as f:
                self.key = f.read()
            activated, message = keyValidation.main(self.key)
            if activated:
                return
            else:
                self.init_ui()
                self.setLayout(self.layout1)
                self.exec()
        except:
            self.init_ui()
            self.setLayout(self.layout1)
            self.exec()
        

    def init_ui(self):
        self.resize(600, 100)
        self.center()
        self.setWindowTitle("AutoZoom")
        self.layout1 = QVBoxLayout()
        self.layout2 = QHBoxLayout()
        self.key_input = QLineEdit()
        self.prompt = QLabel('Please enter your key below. Press Enter to confirm.')
        self.prompt.setAlignment(Qt.AlignCenter)
        self.layout2.addSpacing(100)
        self.layout1.addWidget(self.prompt)
        self.layout1.addLayout(self.layout2)
        self.layout2.addWidget(self.key_input)
        self.layout2.addSpacing(100)
        self.key_input.returnPressed.connect(self.checkKey)

    def checkKey(self):
        activated, message = keyValidation.main(self.key_input.text())
        if activated == False:
            self.prompt.setText('Invalid key. Please enter a valid key below.')
        if activated == True:
            self.hide()


    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    def closeEvent(self,event):
        sys.exit()

class MainWindow(QMainWindow):
      
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.showDialog()
        self.init_ui()
        self.loadConfig()
        self.updateTabNames()

    def showDialog(self):
        KeyWindow()

    def loadConfig(self):
        config_file = getPath('.config')
        try:
            with open(config_file) as json_file:
                self.classes = json.load(json_file)
                restoreSettings.main(qApp,self.classes)
                if self.classes == {}:
                    self.addClass()
        except:
            self.addClass()        

    def init_ui(self):
        self.classes = {}
        self.resize(600, 200)
        self.center()
        self.setWindowTitle("AutoZoom")
        self.tabWidget = QTabWidget()
        self.tabWidget.tabBar().setSelectionBehaviorOnRemove(1)
        icon_location = getPath('autoZoomIcon.png')
        self.setWindowIcon(QIcon(icon_location))
        self.layout1 = QVBoxLayout()
        add_remove_layout = QHBoxLayout()
        self.layout1.addLayout(add_remove_layout)
        add_class_button = QPushButton('Add Class', self)
        remove_class_button = QPushButton('Remove Class', self)
        add_remove_layout.addWidget(add_class_button)
        add_remove_layout.addWidget(remove_class_button)
        self.layout1.addWidget(self.tabWidget)
        add_class_button.clicked.connect(self.addClass)
        remove_class_button.clicked.connect(self.removeClass)
        save_button = QPushButton('Save',self)
        self.layout1.addWidget(save_button)
        save_button.clicked.connect(self.saveData)
        
        widget = QWidget()
        widget.setLayout(self.layout1)

        self.setCentralWidget(widget)

    def addClass(self):
        self.updateTabNames()
        if self.tabWidget.count() == 7: 
            WarningDialog('You can\'t have more than 7 classes.')
            return
        tab = Tab()
        start_time = tab.start_time.time()
        end_time = tab.end_time.time()

        title = 'Class {}'.format(self.tabWidget.count()+1)
        tab.class_name.setText(title)
        self.classes[title]={}
        self.classes[title]['link']=tab.zoom_link.text()
        self.classes[title]['days']=[None]*7
        self.classes[title]['start_time']=[start_time.hour(), start_time.minute()]
        self.classes[title]['end_time']=[end_time.hour(), end_time.minute()]
        self.tabWidget.addTab(tab,title)
        self.tabWidget.setCurrentWidget(tab)
        self.updateTabNames()

    def removeClass(self):
        tab_ind = self.tabWidget.currentIndex()
        if self.tabWidget.count() == 1:
            confirmation = ClearDialog('Do you want to clear all classes?')
            if confirmation.canceled == False:
                self.classes.pop(self.tabWidget.tabText(tab_ind))
                self.tabWidget.removeTab(tab_ind)
                self.close()
                
        else:
            self.classes.pop(self.tabWidget.tabText(tab_ind))
            self.tabWidget.removeTab(tab_ind)

            self.updateTabNames()

    def saveData(self):
        tab_count = self.tabWidget.count()
        #go through each tab and compare tab text to each tab title
        #what if they enter the same class in tabs before they save
        z = (self.tabWidget.currentIndex(),)
        for i in range(tab_count):
            current_tab = self.tabWidget.widget(i)
            class_name = current_tab.class_name.text() #text in the input field
    
            for j in range(tab_count):
                self.tabWidget.setCurrentIndex(j)
                current_widg = self.tabWidget.widget(j)
                current_class_name = current_widg.class_name.text()

                if class_name == current_class_name: #or class_name in self.classes.keys():
                    if current_widg != current_tab: #if current tab isnt the saving tab
                        """
                        You need to see why the tab text changes after you try and change 
                        class name to an existing one. It seems like it changes even though it shouldn't
                        tha fuck is this shit. goodnight

                        """
                        WarningDialog('You can\'t have two classes with the same name!')
                        
                        self.tabWidget.setCurrentWidget(current_widg) #set the current tab = saving tab
                        self.updateTabNames()
                        self.tabWidget.setCurrentWidget(self.tabWidget.widget(z[0]))
                        return 1
            if current_tab.class_name.text() != '':
               self.classes[class_name] = self.classes.pop(self.tabWidget.tabText(i)) #overwrites current class name w new one. For updating names and links
            
            zoom_link = current_tab.zoom_link.text()
            checked = [None]*7
            for j in range(0,7):
                if current_tab.day_widgets[j].isChecked():
                    checked[j] = 1
                else:
                    checked[j] = 0
            start_time = current_tab.start_time.time()
            end_time = current_tab.end_time.time()
            self.tabWidget.setTabText(i,class_name)
            self.classes[class_name]={}
            self.classes[class_name]['link'] = zoom_link
            self.classes[class_name]['days'] = checked
            self.classes[class_name]['start_time'] = [start_time.hour(), start_time.minute()]
            self.classes[class_name]['end_time'] = [end_time.hour(), end_time.minute()]
        self.tabWidget.setCurrentWidget(self.tabWidget.widget(z[0]))

    def updateTabNames(self):
        for i in range(0,self.tabWidget.count()):
            if 'Class' in self.tabWidget.tabText(i):
                title = 'Class {}'.format(i+1)
                self.classes[title] = self.classes.pop(self.tabWidget.tabText(i))
                self.tabWidget.setTabText(i,title)
                self.tabWidget.setCurrentIndex(i)
                tab = self.tabWidget.currentWidget()
                tab.class_name.setText(title)

    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())


    def closeEvent(self, event):
        if self.classes != {}:
            success = self.saveData()
            if success == 1:
                event.ignore()
        config_file = getPath('.config')
        with open(config_file,'w') as json_file:
            json.dump(self.classes, json_file)
        QMainWindow.closeEvent(self, event)
        makeCron.main(self.classes)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowFlags(Qt.WindowStaysOnTopHint)
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()



