import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from conn import *

class ClickableLabel(QLabel):
    clicked = pyqtSignal(str)

    def __init__(self,image_path,identifier,parent=None):
        super().__init__(parent)
        
        self.identifier = identifier
        self.setFixedSize(200, 200)
        
        # Cargar y escalar la imagen
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(
            self.size(), 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
        )
        
        self.setPixmap(pixmap)
        self.setScaledContents(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.identifier)

class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.inicializarUI()
        self.textito()
        self.cuadritos()


    def inicializarUI(self):
        self.setGeometry(100, 100, 1300, 800)
        self.setWindowTitle("Boletitos")
        self.layout_principal = QVBoxLayout()
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout = QGridLayout()  
        self.layout_principal.addLayout(self.layout)
        self.setLayout(self.layout_principal)
        self.show()

    def cuadritos(self):
        # Creamos 8 etiquetas con imágenes
        image_info = [
            ("images/kendrick.jpg", "Kendrick"),
            ("images/latinmafia.jpg", "Latin Mafia"),
            ("images/chicossuicidas.jpg", "Chicos Suicidas"),
            ("images/feid.jpg", "Feid"),
            ("images/kanye.jpg", "Kanye"),
            ("images/mora.jpg", "Mora"),
            ("images/miko.jpg", "Miko"),
            ("images/ote.jpg", "OTE"),
        ]
        for i, (path,identifier) in enumerate(image_info):
            # Crear ClickableLabel en lugar de QLabel
            label = ClickableLabel(path, identifier, self)
            
            # Conectar la señal de clic
            label.clicked.connect(self.abrir_ventana_album)
            
            # Añadir al grid (2 filas x 4 columnas)
            fila = i // 4
            columna = i % 4
            self.layout.addWidget(label, fila, columna)
    
    def textito(self):
        label = QLabel("Conciertos disponibles en tu ciudad", self)
        label.setFont(QFont("Arial", 16, QFont.Weight.Bold))  # Cambia la fuente y tamaño
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrado del texto
        self.layout_principal.insertWidget(0, label)

    def abrir_ventana_album(self, identifier):
        # Crear una nueva ventana para el álbum
        ventana_album = QDialog(self)
        ventana_album.setGeometry(100, 100, 600, 400)
        ventana_album.setWindowTitle(f"Concierto de: {identifier}")
        
        # Ejemplo de contenido para la ventana
        layout_album = QVBoxLayout()    
        
        # Título del álbum
        titulo = QLabel(f"Fila para boletos: {identifier}")
        titulo.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Puedes agregar más widgets aquí
        layout_album.addWidget(titulo)
        ventana_album.setLayout(layout_album)
        ventana_album.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana()
    sys.exit(app.exec())