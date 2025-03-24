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
        self.setGeometry(100, 100, 1300, 800)
        self.setWindowTitle("Boletitos")
        self.layout = QGridLayout()  # Cambiamos a QGridLayout para organizar en filas y columnas
        self.setLayout(self.layout)
        self.show()

    def cuadritos(self):
        # Creamos 8 etiquetas con imágenes
        image_paths = [
            "images/kendrick.jpg",
            "images/latinmafia.jpg",
            "images/chicossuicidas.jpg",
            "images/feid.jpg",
            "images/kanye.jpg",
            "images/mora.jpg",
            "images/miko.jpg",
            "images/ote.jpg",
        ]
        for i in range(8):
            label = QLabel(self)  # Creamos una nueva etiqueta
            label.setFixedSize(200, 200)

            # Cargamos la imagen (puedes personalizar las imágenes con una lista si quieres diferentes)
            pixmap = QPixmap(image_paths[i])
            pixmap = pixmap.scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            label.setPixmap(pixmap)
            label.setScaledContents(True)

            # Añadimos la etiqueta al grid (2 filas x 4 columnas)
            fila = i // 4
            columna = i % 4
            self.layout.addWidget(label, fila, columna)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana()
    sys.exit(app.exec())