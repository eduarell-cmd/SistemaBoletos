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
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.show()

    def cuadritos(self):
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

        h_layout = QHBoxLayout()  # Layout horizontal para alinearlas en fila
        h_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrar imágenes

        for path in image_paths:
            label = QLabel(self)
            label.setFixedSize(150, 150)  # Tamaño ajustable para cada imagen
            pixmap = QPixmap(path)

            # Ajustar el tamaño de la imagen manteniendo relación de aspecto
            pixmap = pixmap.scaled(
                label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            label.setPixmap(pixmap)
            label.setScaledContents(True)
            h_layout.addWidget(label)

        self.layout.addLayout(h_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    sys.exit(app.exec())
