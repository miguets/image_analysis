import cv2
import io
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

class ProcesadorImagenes:
    def __init__(self):
        # Mapas personalizados
        mis_colores = [(0.0, 0.0, 0.0), (0.0, 0.1, 0.5), (1.0, 0.0, 0.0)]
        self.mi_mapa = LinearSegmentedColormap.from_list("MiMapa", mis_colores, N=256)

        colores_pastel = [(1.0, 0.8, 0.9), (0.8, 1.0, 0.8), (0.8, 0.9, 1.0), (1.0, 1.0, 0.8), (0.9, 0.8, 1.0)]
        self.mapa_pastel = LinearSegmentedColormap.from_list("PastelMap", colores_pastel, N=256)

        self.mapas = {
            "Grises": "gray", "JET": "jet", "HOT": "hot",
            "OCEAN": "ocean", "BONE": "bone", "PINK": "pink",
            "Pastel": self.mapa_pastel, "MiMapa": self.mi_mapa
        }

        # Estado de las imágenes
        self.imagen_original = None
        self.imagen_anterior = None
        self.imagen_nueva = None

    def obtener_nombres_mapas(self):
        return list(self.mapas.keys())

    def cargar_imagen(self, ruta):
        self.imagen_original = cv2.imread(ruta)
        self.imagen_anterior = None
        self.imagen_nueva = None
        return self.imagen_original

    def aplicar_mapa_color(self, nombre_mapa):
        if self.imagen_original is None:
            return False

        # Mover la imagen nueva a la anterior antes de generar la nueva
        if self.imagen_nueva is not None:
            self.imagen_anterior = self.imagen_nueva.copy()

        gris = cv2.cvtColor(self.imagen_original, cv2.COLOR_BGR2GRAY)

        plt.figure(figsize=(3, 3))
        plt.imshow(gris, cmap=self.mapas[nombre_mapa])
        plt.axis("off")

        # Optimización: Guardar en buffer de memoria en lugar de crear un archivo 'temp.png'
        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches='tight', pad_inches=0)
        plt.close()
        buf.seek(0)

        # Leer la imagen desde la memoria
        file_bytes = np.asarray(bytearray(buf.read()), dtype=np.uint8)
        self.imagen_nueva = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        return True