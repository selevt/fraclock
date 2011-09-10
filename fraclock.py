import clockbase
import optparse
import sys
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL, QTimer, QObject, Qt

class MainWindow(QtGui.QWidget):
  def __init__(self, on_top=False, parent=None):
    QtGui.QWidget.__init__(self, parent)
    
    if on_top:
      self.setWindowFlags(Qt.WindowFlags() | Qt.WindowStaysOnTopHint)
    
    self.setWindowTitle("fraclock")
    self.setWindowIcon(QtGui.QIcon('icon.png'))
    
    self.cur_time_button = QtGui.QPushButton(self.tr("Current Time"))
    self.convert_time_button = QtGui.QPushButton(self.tr("Convert Time"))
    self.copy_button = QtGui.QPushButton(self.tr("Copy"))

    buttonlayout = QtGui.QHBoxLayout()
    buttonlayout.addWidget(self.cur_time_button)
    buttonlayout.addWidget(self.convert_time_button)
    buttonlayout.addWidget(self.copy_button)
    
    self.clock_scene = QtGui.QGraphicsScene()
    self.clock_text = QtGui.QGraphicsTextItem("", None, self.clock_scene) 
    self.clock_text.setFont(QtGui.QFont("Verdana", 12));    
    self.clock_view = QtGui.QGraphicsView(self.clock_scene)
    
    mainlayout = QtGui.QVBoxLayout()
    mainlayout.addLayout(buttonlayout)
    mainlayout.addWidget(self.clock_view)        
    self.setLayout(mainlayout)

    self.timer = QTimer()
    QObject.connect(self.timer, SIGNAL("timeout()"), self.update_time)
    QObject.connect(self.cur_time_button, SIGNAL("clicked()"), self.start_timer)
    QObject.connect(self.convert_time_button, SIGNAL("clicked()"), self.convert_time)    
    QObject.connect(self.copy_button, SIGNAL("clicked()"), self.copy_to_clipboard)


  def update_time(self):
    self.set_clock_text(clockbase.get_current_time())
    self.update()
    
  def start_timer(self):
    self.update_time()
    self.timer.start(1000)
  
  def set_clock_text(self, text):
    self.clock_text.setPlainText(text)
    
  def copy_to_clipboard(self):
    QtGui.QApplication.clipboard().setText(self.clock_text.toPlainText())
  
  def convert_time(self):
    self.timer.stop()
    usual_time, ok = QtGui.QInputDialog.getText(self, self.tr("Convert Time"), self.tr("Enter the time you want to convert to fraclock time"), text="usage: hh:mm[:ss]")
    usual_time = usual_time.replace(' ',':')
    parts = usual_time.split(":")
    if(len(parts) < 2 or len(parts) > 3):
      self.set_clock_text(self.tr("usage: hh:mm[:ss]"))
    else:
      if(len(parts) == 3):
          hour, minute, sec = parts
      elif(len(parts) == 2):
          hour, minute = parts
          sec = 0
      try:
        hour, min, sec = int(hour), int(minute), int(sec)
        self.set_clock_text(clockbase.get_time(hour, min, sec))
      except Exception:
        self.set_clock_text(self.tr("invalid input data"))
    
if __name__ == '__main__':

  optp = optparse.OptionParser()
  optp.add_option('--ontop', '-o', dest="ontop", action="store_true", help="specify if window should be always on top")
  
  options, arguments = optp.parse_args()
  ot = False
  if options.ontop:
    ot = True

  app = QtGui.QApplication(sys.argv)
  main_window = MainWindow(on_top=ot)
  main_window.show()
  main_window.start_timer()
  sys.exit(app.exec_())
