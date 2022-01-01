from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

class poggers(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Preferred
        )

        self.data = 48
        self.rate = 1
        self.min,self.max = 0,800

    # def sizeHint(self):
    #     return QtCore.QSize(800,500)\

    def paintEvent(self, e):
        self.data+=self.rate
        self.data=max(min(self.max,self.data),self.min)
        painter = QtGui.QPainter(self)
        #painter.setPen(QtGui.QColor("NoColor"))
        #print("googers")
        zz = min(painter.device().minimumWidth(), painter.device().minimumHeight())
        pp = max(min(painter.device().width(),painter.device().height()),zz)
        #pp = (w**2 + h**2)**0.5
        w,h = pp,pp
        lnwidth = 20
        mm = 2

        brush = QtGui.QBrush(QtGui.QColor("NoColor"))


        #brush.setColor(QtGui.QLinearGradient(0,0,1,1))
        #brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        rect = QtCore.QRectF(lnwidth*mm/2, lnwidth*mm/2, w-lnwidth*mm,h-lnwidth*mm)
        

        pen = QtGui.QPen(brush,lnwidth*mm,cap=Qt.RoundCap)
        painter.setPen(pen)
        painter.drawArc(
            rect,
            -40*16,
            260*16
        )
    

        brush = QtGui.QBrush()
        red = (self.data-self.min)/(self.max-self.min)
        green = 1-red
        brush.setColor(QtGui.QColor.fromRgb(int(red*255),int(green*255),int(red*150)))
        brush.setStyle(Qt.SolidPattern)

        painter.setBrush(brush)
        pen = QtGui.QPen(brush,lnwidth,cap=Qt.RoundCap)

        painter.setPen(pen)

        margin = (lnwidth*mm)-lnwidth
        rect = QtCore.QRectF(
            (margin/2+lnwidth/2),
            (margin/2+lnwidth/2),
            h-(lnwidth+margin),
            h-(lnwidth+margin)
        )

        painter.drawArc(
            rect,
            220*16,#-40*16,
            int(((self.data - self.min)/self.max)*-260*16)
        )

        font = painter.font()
        font.setPixelSize(48)
        font.setBold(True)
        painter.setFont(font)
        fm = QtGui.QFontMetrics(font)
        t = f"[{int(self.data)}/{self.max}]"
        if w/2-fm.horizontalAdvance(t)/2 <lnwidth*mm+lnwidth:
            return None
        rect = QtCore.QRectF(
            w/2-fm.horizontalAdvance(t)/2,
            h/2-fm.height(),
            fm.horizontalAdvance(t),
            fm.height()
        )
        painter.drawText(rect,Qt.AlignHCenter, t)

        painter.end()

    def _trigger_refresh(self):
        self.update()


import sys
app = QtWidgets.QApplication()#sys.argv)
window = QtWidgets.QMainWindow()
#window.setLayout(QtWidgets.QVBoxLayout())
volume = poggers()
volume.show()
#window.show()
app.exec_()

## Please ignore any ugly code!