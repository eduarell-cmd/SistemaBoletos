import sys 
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from conn import *


class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.inicializarUI()
        self.cuadritos()

    def inicializarUI(self):
        self.setGeometry(100,100,1300,800)
        self.setWindowTitle("Boletitos")
        self.layout = QVBoxLayout()  
        self.setLayout(self.layout)  
        self.show()
    
    def cuadritos(self):
        self.label=QLabel(self)
        self.label.setFixedSize(200, 200)
        pixmap = QPixmap("nata.jpg")  
        pixmap = pixmap.scaled(self.label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)
        self.label.move(20,20)
        self.label.show()

if __name__ == '__main__':
    app=QApplication(sys.argv)
    ventana=Ventana()
    sys.exit(app.exec())