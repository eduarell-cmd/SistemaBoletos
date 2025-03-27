import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from conn import *
from collections import deque
from typing import List, Dict
import time

class Ticket:
    def __init__(self, id: str, categoria: str, precio: float, artista: str, fecha: str):
        self.id = id
        self.categoria = categoria
        self.precio = precio
        self.artista = artista
        self.fecha = fecha
        self.comprado = False
        self.timestamp = time.time()

class TicketManager:
    def __init__(self):
        
        self.cola_espera = deque()
        self.boletos_disponibles: Dict[str, List[Ticket]] = {}
        self.historial_compras = []
        
    def inicializar_boletos(self, artista: str, fecha: str):
        # Crear boletos para cada categoría
        boletos = []
        precios = {
            "VIP": 3000,
            "Platino": 2500,
            "Oro": 2000,
            "General": 1000
        }
        
        # Obtener iniciales del artista
        iniciales = ''.join(palabra[0] for palabra in artista.split())
        
        contador = 1
        for categoria, precio in precios.items():
            for i in range(10):  
                # Ejemplo: KL-V001 (Kendrick Lamar - VIP - 001)
                id_boleto = f"{iniciales}-{categoria[0]}{contador:03d}"
                ticket = Ticket(
                    id_boleto,
                    categoria,
                    precio,
                    artista,
                    fecha
                )
                boletos.append(ticket)
                contador += 1
        
        self.boletos_disponibles[artista] = boletos
    
    def agregar_a_cola(self, ticket: Ticket):
        self.cola_espera.append(ticket)
    
    def procesar_siguiente_compra(self) -> Ticket:
        if self.cola_espera:
            ticket_en_cola = self.cola_espera.popleft()
            
            # Buscar un ticket disponible que coincida con la categoría y artista
            if ticket_en_cola.artista in self.boletos_disponibles:
                tickets_artista = self.boletos_disponibles[ticket_en_cola.artista]
                for ticket in tickets_artista:
                    if (not ticket.comprado and 
                        ticket.categoria == ticket_en_cola.categoria):
                        # Marcar el ticket como comprado
                        ticket.comprado = True
                        self.historial_compras.append(ticket)
                        print(f"[DEBUG] Ticket {ticket.id} marcado como comprado")
                        return ticket
            
            print(f"[DEBUG] No se encontró ticket disponible para {ticket_en_cola.artista} - {ticket_en_cola.categoria}")
            return None
        return None
    
    def obtener_disponibilidad(self, artista: str) -> Dict[str, int]:
        if artista not in self.boletos_disponibles:
            return {}
        
        disponibilidad = {}
        for ticket in self.boletos_disponibles[artista]:
            if not ticket.comprado:
                disponibilidad[ticket.categoria] = disponibilidad.get(ticket.categoria, 0) + 1
        
        print(f"[DEBUG] Disponibilidad para {artista}: {disponibilidad}")
        return disponibilidad

class ConcertCard(QWidget):
    clicked = pyqtSignal(str)

    def __init__(self, image_path, identifier, fecha, parent=None):
        super().__init__(parent)
        self.identifier = identifier
        
        # Layout principal de la tarjeta
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # Contenedor de la imagen
        image_container = QLabel()
        image_container.setFixedSize(200, 200)
        
        # Cargar y escalar la imagen
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(
            image_container.size(), 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
        )
        image_container.setPixmap(pixmap)
        image_container.setScaledContents(True)
        
        # Nombre del artista
        nombre_label = QLabel(identifier)
        nombre_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        nombre_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Fecha del concierto
        fecha_label = QLabel(fecha)
        fecha_label.setFont(QFont("Arial", 10))
        fecha_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Agregar widgets al layout
        layout.addWidget(image_container)
        layout.addWidget(nombre_label)
        layout.addWidget(fecha_label)
        
        # Estilo de la tarjeta
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 10px;
                border: 2px solid #ddd;
            }
            QWidget:hover {
                border: 2px solid #4CAF50;
            }
        """)
        
        self.setLayout(layout)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(220, 280)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Asegurarse de que la ventana principal esté activa antes de emitir la señal
            if self.parent() and self.parent().parent():
                self.parent().parent().activateWindow()
            self.clicked.emit(self.identifier)

class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.ticket_manager = TicketManager()
        self.inicializarUI()
        self.textito()
        self.cuadritos()
        self.blur_effect = None
        
        # Inicializar boletos para todos los conciertos
        concert_info = [
            ("Kendrick Lamar", "15 Mayo 2024"),
            ("Latin Mafia", "20 Mayo 2024"),
            ("Chicos Suicidas", "25 Mayo 2024"),
            ("Feid", "30 Mayo 2024"),
            ("Kanye West", "5 Junio 2024"),
            ("Mora", "10 Junio 2024"),
            ("Miko", "15 Junio 2024"),
            ("OTE", "20 Junio 2024"),
        ]
        
        for artista, fecha in concert_info:
            self.ticket_manager.inicializar_boletos(artista, fecha)

    def inicializarUI(self):
        self.setGeometry(100, 100, 1300, 800)
        self.setWindowTitle("Boletitos")
        self.layout_principal = QVBoxLayout()
        self.layout_principal.setContentsMargins(20, 20, 20, 20)  # Agregar márgenes
        self.layout = QGridLayout()  
        self.layout_principal.addLayout(self.layout)
        
        # Crear un widget para el botón de admin al final
        admin_widget = QWidget()
        admin_layout = QHBoxLayout()
        admin_layout.setContentsMargins(0, 20, 0, 0)  # Más espacio arriba
        
        # Crear el botón de administración con nuevo estilo
        boton_admin = QPushButton("ADMIN 👤", self)
        boton_admin.setFont(QFont("Arial", 14, QFont.Weight.Bold))  # Fuente más grande y negrita
        boton_admin.setStyleSheet("""
            QPushButton {
                background-color: #1976D2;
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 8px;
                min-width: 200px;
                letter-spacing: 2px;  /* Espaciado entre letras */
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        boton_admin.setCursor(Qt.CursorShape.PointingHandCursor)
        boton_admin.clicked.connect(self.abrir_panel_admin)
        
        # Agregar el botón al layout centrado
        admin_layout.addStretch()
        admin_layout.addWidget(boton_admin)
        admin_layout.addStretch()  # Agregar otro stretch para centrar
        admin_widget.setLayout(admin_layout)
        
        # Agregar el widget de admin al final del layout principal
        self.layout_principal.addWidget(admin_widget)
        
        self.setLayout(self.layout_principal)
        self.show()

    def cuadritos(self):
        print("\n[DEBUG] Inicializando cuadritos")
        # Creamos 8 tarjetas con información de conciertos
        concert_info = [
            ("images/kendrick.jpg", "Kendrick Lamar", "15 Mayo 2024"),
            ("images/latinmafia.jpg", "Latin Mafia", "20 Mayo 2024"),
            ("images/chicossuicidas.jpg", "Chicos Suicidas", "25 Mayo 2024"),
            ("images/feid.jpg", "Feid", "30 Mayo 2024"),
            ("images/kanye.jpg", "Kanye West", "5 Junio 2024"),
            ("images/mora.jpg", "Mora", "10 Junio 2024"),
            ("images/miko.jpg", "Miko", "15 Junio 2024"),
            ("images/ote.jpg", "OTE", "20 Junio 2024"),
        ]
        
        for i, (path, identifier, fecha) in enumerate(concert_info):
            print(f"[DEBUG] Creando tarjeta para {identifier}")
            # Crear ConcertCard en lugar de ClickableLabel
            card = ConcertCard(path, identifier, fecha, self)
            
            # Conectar la señal de clic
            card.clicked.connect(self.abrir_ventana_album)
            
            # Añadir al grid (2 filas x 4 columnas)
            fila = i // 4
            columna = i % 4
            self.layout.addWidget(card, fila, columna)
        print("[DEBUG] Cuadritos inicializados")
    
    def textito(self):
        # Crear un contenedor para el título
        titulo_container = QWidget()
        titulo_layout = QVBoxLayout()
        titulo_layout.setContentsMargins(0, 20, 0, 20)  # Márgenes verticales
        
        # Título principal
        label = QLabel("DonDimadonBoleton", self)
        label.setFont(QFont("Arial", 32, QFont.Weight.Bold))  # Fuente más grande
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Estilo del título
        label.setStyleSheet("""
            QLabel {
                color: #1976D2;  /* Color azul */
                padding: 10px 20px;
                background-color: #E3F2FD;  /* Fondo azul claro */
                border-radius: 15px;
                margin: 10px;
            }
        """)
        
        # Subtítulo
        subtitulo = QLabel("Tu Boletera de Confianza", self)
        subtitulo.setFont(QFont("Arial", 16))
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitulo.setStyleSheet("color: #666;")  # Color gris para el subtítulo
        
        # Agregar widgets al layout
        titulo_layout.addWidget(label)
        titulo_layout.addWidget(subtitulo)
        titulo_container.setLayout(titulo_layout)
        
        # Agregar el contenedor al layout principal
        self.layout_principal.insertWidget(0, titulo_container)

    def aplicar_blur(self):
        print("[DEBUG] Creando nuevo efecto de desenfoque")
        self.blur_effect = QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(10)  # Aplicar desenfoque
        self.setGraphicsEffect(self.blur_effect)

    def remover_blur(self):
        print("[DEBUG] Removiendo efecto de desenfoque")
        if self.blur_effect:
            self.blur_effect.setBlurRadius(0)
            self.setGraphicsEffect(None)
            self.blur_effect = None  

    def abrir_ventana_album(self, identifier):
        print(f"\n[DEBUG] Abriendo ventana de álbum para {identifier}")

        self.activateWindow()
        self.aplicar_blur()
        
        ventana_album = QDialog(self)
        ventana_album.setGeometry(100, 100, 800, 600)
        ventana_album.setWindowTitle(f"Concierto de: {identifier}")
        
    
        ventana_album.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
        ventana_album.setModal(True)
        
  
        main_geometry = self.geometry()
        

        x = main_geometry.x() + (main_geometry.width() - ventana_album.width()) // 2
        y = main_geometry.y() + (main_geometry.height() - ventana_album.height()) // 2
        
 
        ventana_album.move(x, y)
        
      
        layout_album = QVBoxLayout()    
        
   
        titulo = QLabel(f"Concierto de {identifier}")
        titulo.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_album.addWidget(titulo)
        
        
        info_frame = QFrame()
        info_frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        info_layout = QVBoxLayout()
        
     
        fecha_label = QLabel(f"📅 Fecha: 15 de mayo")
        lugar_label = QLabel(f"📍 Lugar: Arena Ciudad de México")
        fecha_label.setFont(QFont("Arial", 12))
        lugar_label.setFont(QFont("Arial", 12))
        info_layout.addWidget(fecha_label)
        info_layout.addWidget(lugar_label)
        
    
        hora_label = QLabel("🕒 Hora: 20:00")
        hora_label.setFont(QFont("Arial", 12))
        info_layout.addWidget(hora_label)
        
        info_frame.setLayout(info_layout)
        layout_album.addWidget(info_frame)
        
        
        precios_frame = QFrame()
        precios_frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        precios_layout = QVBoxLayout()
        
        precios_titulo = QLabel("Precios y Disponibilidad")
        precios_titulo.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        precios_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        precios_layout.addWidget(precios_titulo)
        
        
        disponibilidad = self.ticket_manager.obtener_disponibilidad(identifier)
        
        
        precios = [
            ("VIP", "$3,000"),
            ("Platino", "$2,500"),
            ("Oro", "$2,000"),
            ("General", "$1,000")
        ]
        
        
        radio_group = QButtonGroup(ventana_album)
        
        
        cantidad_spinner = QSpinBox()
        cantidad_spinner.setMinimum(1)
        cantidad_spinner.setMaximum(4)
        cantidad_spinner.setEnabled(False)
        
        
        cantidad_frame = QFrame()
        cantidad_layout = QHBoxLayout()
        cantidad_layout.setContentsMargins(10, 10, 10, 10)
        
        cantidad_label = QLabel("Cantidad de boletos:")
        cantidad_label.setFont(QFont("Arial", 12))
        cantidad_layout.addWidget(cantidad_label)
        cantidad_layout.addWidget(cantidad_spinner)
        cantidad_layout.addStretch()
        
        cantidad_frame.setLayout(cantidad_layout)
        
        for zona, precio in precios:
            precio_widget = QWidget()
            precio_layout = QHBoxLayout()
            precio_layout.setContentsMargins(0, 0, 0, 0)
            
            radio_button = QRadioButton()
            radio_button.setText(zona)
            disponibles = disponibilidad.get(zona, 0)
            radio_button.setEnabled(disponibles > 0)
            radio_group.addButton(radio_button)
            
            precio_label = QLabel(precio)
            disponibilidad_label = QLabel(f"Disponibles: {disponibles}")
            
            def toggle_spinner(checked, disponibles):
                cantidad_spinner.setEnabled(checked)
                if checked:
                    cantidad_spinner.setMaximum(min(4, disponibles))
            radio_button.toggled.connect(lambda checked, d=disponibles: toggle_spinner(checked, d))
            
            radio_button.setFont(QFont("Arial", 12))
            precio_label.setFont(QFont("Arial", 12))
            disponibilidad_label.setFont(QFont("Arial", 12))
            
            precio_layout.addWidget(radio_button)
            precio_layout.addStretch()
            precio_layout.addWidget(precio_label)
            precio_layout.addWidget(disponibilidad_label)
            
            precio_widget.setLayout(precio_layout)
            precios_layout.addWidget(precio_widget)
        
        precios_layout.addWidget(cantidad_frame)
        precios_frame.setLayout(precios_layout)
        layout_album.addWidget(precios_frame)
        
        cola_frame = QFrame()
        cola_frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        cola_layout = QVBoxLayout()
        
        cola_titulo = QLabel("Estado de la Cola")
        cola_titulo.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        cola_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cola_layout.addWidget(cola_titulo)
        
        personas_en_cola = len(self.ticket_manager.cola_espera)
        cola_info = QLabel(f"Personas en espera: {personas_en_cola}")
        cola_info.setFont(QFont("Arial", 12))
        cola_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cola_layout.addWidget(cola_info)
        
        cola_frame.setLayout(cola_layout)
        layout_album.addWidget(cola_frame)
        
        
        boton_comprar = QPushButton("Comprar Boletos")
        boton_comprar.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        boton_comprar.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 15px 32px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        
        
        def comprar_con_categoria():
            print(f"[DEBUG] Botón de compra presionado")
            categoria_seleccionada = radio_group.checkedButton()
            if categoria_seleccionada:
                categoria = categoria_seleccionada.text()
                cantidad = cantidad_spinner.value()
                print(f"[DEBUG] Categoría seleccionada: {categoria}, Cantidad: {cantidad}")
                if self.comprar_boletos(identifier, categoria, cantidad):
                    print(f"[DEBUG] Compra exitosa, cerrando ventana de álbum")
                    ventana_album.done(QDialog.DialogCode.Accepted)
            else:
                print(f"[DEBUG] No se seleccionó categoría")
                QMessageBox.warning(
                    ventana_album,
                    "Selección Requerida",
                    "Por favor, selecciona una categoría de boleto."
                )
        
        boton_comprar.clicked.connect(comprar_con_categoria)
        layout_album.addWidget(boton_comprar)
        
        
        def on_finished():
            print(f"[DEBUG] Ventana de álbum cerrada, limpiando recursos")
            self.remover_blur()
            ventana_album.deleteLater()
            self.activateWindow()
            print(f"[DEBUG] Recursos limpiados, ventana principal activada")
        
        ventana_album.finished.connect(on_finished)
        ventana_album.setLayout(layout_album)
        
        print(f"[DEBUG] Ejecutando diálogo de álbum")
        ventana_album.exec()
        print(f"[DEBUG] Diálogo de álbum finalizado")
    
    def comprar_boletos(self, artista, categoria, cantidad=1):
        print(f"\n[DEBUG] Iniciando compra de {cantidad} boletos para {artista} - {categoria}")
        
        tickets_comprados = []
        for _ in range(cantidad):
            
            precios = {
                "VIP": 3000,
                "Platino": 2500,
                "Oro": 2000,
                "General": 1000
            }
            
           
            iniciales = ''.join(palabra[0] for palabra in artista.split())
            
            id_temporal = f"{iniciales}-{categoria[0]}{int(time.time())%1000:03d}"
            
            ticket = Ticket(
                id_temporal,
                categoria,
                precios[categoria],
                artista,
                "15 Mayo 2024"  
            )
            print(f"[DEBUG] Ticket creado: {ticket.id}")
            
            
            self.ticket_manager.agregar_a_cola(ticket)
            
        
            ticket_comprado = self.ticket_manager.procesar_siguiente_compra()
            if ticket_comprado:
                tickets_comprados.append(ticket_comprado)
            else:
                break
        
        if tickets_comprados:
            print(f"[DEBUG] Compra exitosa de {len(tickets_comprados)} boletos")
            # Mensaje de comprado
            mensaje = f"¡Compra exitosa!\n\nArtista: {artista}\nCategoría: {categoria}\n"
            mensaje += f"Cantidad: {len(tickets_comprados)}\n"
            mensaje += f"Total: ${len(tickets_comprados) * precios[categoria]:,.2f}\n\n"
            mensaje += "IDs de boletos:\n"
            for ticket in tickets_comprados:
                mensaje += f"- {ticket.id}\n"
            
            QMessageBox.information(
                self,
                "Compra de Boletos",
                mensaje,
                QMessageBox.StandardButton.Ok
            )
            print(f"[DEBUG] Mensaje de éxito mostrado")
            return True
        else:
            print(f"[DEBUG] Compra fallida - No hay suficientes boletos disponibles")
            QMessageBox.warning(
                self,
                "Compra de Boletos",
                "Lo sentimos, no hay suficientes boletos disponibles en esta categoría."
            )
            return False

    def abrir_panel_admin(self):
        print("[DEBUG] Abriendo panel de administración")
        ventana_admin = QDialog(self)
        ventana_admin.setWindowTitle("Panel de Administración")
        ventana_admin.setGeometry(200, 200, 800, 600)
        
        
        layout = QVBoxLayout()
        
        
        titulo = QLabel("Historial de Ventas")
        titulo.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)
        
        # Crear tabla
        tabla = QTableWidget()
        tabla.setColumnCount(6)
        tabla.setHorizontalHeaderLabels(["ID Ticket", "Artista", "Categoría", "Precio", "Fecha", "Hora de Compra"])
        

        tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) 
        tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        tabla.setAlternatingRowColors(True)
        tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
   
        historial = self.ticket_manager.historial_compras
        tabla.setRowCount(len(historial))
        
        for i, ticket in enumerate(historial):
            # Formatear la fecha y hora
            fecha_hora = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ticket.timestamp))
            
            tabla.setItem(i, 0, QTableWidgetItem(ticket.id))
            tabla.setItem(i, 1, QTableWidgetItem(ticket.artista))
            tabla.setItem(i, 2, QTableWidgetItem(ticket.categoria))
            tabla.setItem(i, 3, QTableWidgetItem(f"${ticket.precio}"))
            tabla.setItem(i, 4, QTableWidgetItem(ticket.fecha))
            tabla.setItem(i, 5, QTableWidgetItem(fecha_hora))
        
        layout.addWidget(tabla)
        
        
        stats_frame = QFrame()
        stats_frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        stats_layout = QVBoxLayout()
        
        
        total_ventas = len(historial)
        ingresos_totales = sum(ticket.precio for ticket in historial)
        ventas_por_categoria = {}
        for ticket in historial:
            ventas_por_categoria[ticket.categoria] = ventas_por_categoria.get(ticket.categoria, 0) + 1
        
        
        stats_titulo = QLabel("Estadísticas de Ventas")
        stats_titulo.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        stats_layout.addWidget(stats_titulo)
        
        stats_layout.addWidget(QLabel(f"Total de boletos vendidos: {total_ventas}"))
        stats_layout.addWidget(QLabel(f"Ingresos totales: ${ingresos_totales:,.2f}"))
        
        for categoria, cantidad in ventas_por_categoria.items():
            stats_layout.addWidget(QLabel(f"Boletos {categoria}: {cantidad}"))
        
        stats_frame.setLayout(stats_layout)
        layout.addWidget(stats_frame)
        
        boton_actualizar = QPushButton("Actualizar Datos")
        boton_actualizar.clicked.connect(lambda: self.actualizar_tabla_admin(tabla))
        layout.addWidget(boton_actualizar)
        
        ventana_admin.setLayout(layout)
        ventana_admin.exec()
    
    def actualizar_tabla_admin(self, tabla):
        print("[DEBUG] Actualizando tabla de administración")
        historial = self.ticket_manager.historial_compras
        tabla.setRowCount(len(historial))
        
        for i, ticket in enumerate(historial):
            fecha_hora = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ticket.timestamp))
            
            tabla.setItem(i, 0, QTableWidgetItem(ticket.id))
            tabla.setItem(i, 1, QTableWidgetItem(ticket.artista))
            tabla.setItem(i, 2, QTableWidgetItem(ticket.categoria))
            tabla.setItem(i, 3, QTableWidgetItem(f"${ticket.precio}"))
            tabla.setItem(i, 4, QTableWidgetItem(ticket.fecha))
            tabla.setItem(i, 5, QTableWidgetItem(fecha_hora))
        
        print("[DEBUG] Tabla actualizada")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana()
    sys.exit(app.exec())