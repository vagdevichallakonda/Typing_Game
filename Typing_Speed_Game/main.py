
#For Loading Ui,Widgets etc
from PyQt5 import QtWidgets,QtCore,uic

#For Threads
from PyQt5.QtCore import QThread,pyqtSignal
import sys

#For App Icon
from PyQt5.QtGui import QIcon

#Modules to generate random stories/jokes
import pyjokes

#For time
import time

#################### Global Variables ####################
org=pyjokes.get_joke()
errors=0
wpm=0
startTime=time.time()
endTime=startTime

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        uic.loadUi('Game.ui',self)
        
        #Setting icon
        self.setWindowIcon(QIcon("App_icon.png"))

        #Setting a story
        self.story.setText(org)

        #Hiding Results and Timer at beggining of the game
        self.FinalResult.hide()
        self.Timerqq.hide()

        #Button Events
        self.startb.clicked.connect(self.startGame)
        self.exitb.clicked.connect(self.exitGame)
        self.playb.clicked.connect(self.playAgain)
    
    #Starting Game    
    def startGame(self):
        global errors,wpm,startTime
        errors=0
        wpm=0
        startTime=time.time()
        self.result.clear()
        self.result.setFocus()
        self.FinalResult.hide()
        self.Timerqq.show()
        self.start_timer()

    #Timers
    def start_timer(self):
        try:
            if self.thread.isRunning():
                self.thread.terminate()
                print()
            else:
                pass
        except Exception:
            pass 
        #Timer Thread 
        try:
            self.thread=Timerthread(60)#Here 60 is Time limit (in Seconds)
        except Exception:
            pass
        self.thread.start(100)
        self.thread.signal.connect(self.change_timer)

    def change_timer(self,val):
        if str(val)!="Time Up":
            self.Timerqq.setText('Time Left : '+str(val)+' sec')
        else:
            self.Timerqq.setText(str(val))
        resqq=list(self.story.text())
        try:
            for i in range(0,len(self.result.text())):
                #self.Score()
                if self.result.text()[i]!=resqq[i]:
                    #Setting Red Color
                    self.story.setStyleSheet("font: 20pt \"Sudo\";\n""color: rgb(255,43,43);\n""border: 2px solid;\n""border-top-color : white;\n""border-left-color :white;\n""border-right-color :white;\n""border-bottom-color : white;\n""border-radius:5px;\n""color:rgb(255,43,43);\n""")
                else:
                    #Setting Green Color
                    self.story.setStyleSheet("font: 20pt \"Sudo\";\n""color: rgb(0,168,84);\n""border: 2px solid;\n""border-top-color : white;\n""border-left-color :white;\n""border-right-color :white;\n""border-bottom-color : white;\n""border-radius:5px;\n""color:rgb(0,168,84);\n""")
        except Exception:
            pass
        if self.result.text()==self.story.text():
            self.thread.terminate()
            self.Score()

        if str(val)=='Time Up':
            self.thread.terminate()
            self.Score()

    #Play Again
    def playAgain(self):
        global org
        org=pyjokes.get_joke()
        self.story.setText(org)
        self.startGame()

    #Exiting Game
    def exitGame(self):
        self.close()

    #Calculating Errors
    def Errors(self):
        global errors
        errors=0
        resqq=list(self.story.text())
        try:
            for i in range(0,len(self.result.text())):
                if self.result.text()[i]!=resqq[i]:
                    errors+=1
        except Exception:
            pass
        return(errors)
    
    #Displaying Score
    def Score(self):
        global endTime,startTime,wpm
        endTime=time.time()
        self.timeTaken=int(endTime-startTime)
        wpm=(((len(self.result.text())/5-self.Errors()))/self.timeTaken)*60
        if wpm<0:
            wpm=0
        wpm="{:.2f}".format(wpm)
        
        self.FinalResult.setText(f'Errors :{self.Errors()} WPM :{wpm}')
        self.FinalResult.show()

#Class for implementing Timer Thread
class Timerthread(QThread):
    signal=pyqtSignal(str)
    def __init__(self,limit):
        super(Timerthread,self).__init__()
        self.limit_seconds=limit

    def run(self):
        i=self.limit_seconds
        while i>0:
            self.signal.emit(str(i))
            time.sleep(1)
            i-=1
        self.signal.emit("Time Up")
        

#################### Initialization ####################
app=QtWidgets.QApplication(sys.argv)
main=MainWindow()

#################### Configurations ####################
width=884
height=604
main.setFixedSize(width, height)
main.setWindowTitle("Typing Speed Tester")

main.show()
sys.exit(app.exec_())
