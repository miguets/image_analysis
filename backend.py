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

        # Estado de las imágenes - Práctica 1
        self.imagen_original = None
        self.imagen_anterior = None
        self.imagen_nueva = None

        # Estado de las imágenes - Práctica 2
        self.imagen_p2 = None
        self.componentes_p2 = []
        self.imagen_gris_p2 = None
        self.imagen_binaria_p2 = None

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

    #                   PRÁCTICA 2 

    def _canal_a_imagen(self, canal, cmap):
        """Convierte un canal normalizado (0-1) a imagen BGR usando un colormap de matplotlib."""
        _, ax = plt.subplots(figsize=(3, 3))
        ax.imshow(canal, cmap=cmap, vmin=0, vmax=1)
        ax.axis("off")
        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches='tight', pad_inches=0)
        plt.close()
        buf.seek(0)
        file_bytes = np.asarray(bytearray(buf.read()), dtype=np.uint8)
        return cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    def cargar_imagen_p2(self, ruta):
        self.imagen_p2 = cv2.imread(ruta)
        self.componentes_p2 = []
        self.imagen_gris_p2 = None
        self.imagen_binaria_p2 = None
        return self.imagen_p2

    def separar_componentes_p2(self, modelo):
        if self.imagen_p2 is None:
            return []

        img_rgb = cv2.cvtColor(self.imagen_p2, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0

        if modelo == "RGB":
            canales = [
                (img_rgb[:, :, 0], "Canal R (Rojo)",       "Reds"),
                (img_rgb[:, :, 1], "Canal G (Verde)",       "Greens"),
                (img_rgb[:, :, 2], "Canal B (Azul)",        "Blues"),
            ]
        elif modelo == "CMY":
            C = 1.0 - img_rgb[:, :, 0]
            M = 1.0 - img_rgb[:, :, 1]
            Y = 1.0 - img_rgb[:, :, 2]
            canales = [
                (C, "Canal C (Cian)",     "GnBu"),
                (M, "Canal M (Magenta)",  "RdPu"),
                (Y, "Canal Y (Amarillo)", "YlOrBr"),
            ]
        elif modelo == "HSV":
            img_hsv = cv2.cvtColor(self.imagen_p2, cv2.COLOR_BGR2HSV).astype(np.float32)
            H = img_hsv[:, :, 0] / 179.0
            S = img_hsv[:, :, 1] / 255.0
            V = img_hsv[:, :, 2] / 255.0
            canales = [
                (H, "Canal H (Matiz)",      "hsv"),
                (S, "Canal S (Saturación)", "YlOrRd"),
                (V, "Canal V (Brillo)",     "gray"),
            ]
        else:
            return []

        resultado = [(self._canal_a_imagen(canal, cmap), titulo) for canal, titulo, cmap in canales]
        self.componentes_p2 = resultado
        return resultado

    def convertir_grises_p2(self):
        if self.imagen_p2 is None:
            return None
        self.imagen_gris_p2 = cv2.cvtColor(self.imagen_p2, cv2.COLOR_BGR2GRAY)
        return self.imagen_gris_p2

    def binarizar_p2(self, umbral=None):
        """Si umbral=None usa Otsu (automático), si es int usa umbral fijo."""
        if self.imagen_gris_p2 is None:
            return None, None
        if umbral is None:
            thresh_val, self.imagen_binaria_p2 = cv2.threshold(
                self.imagen_gris_p2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )
        else:
            thresh_val, self.imagen_binaria_p2 = cv2.threshold(
                self.imagen_gris_p2, umbral, 255, cv2.THRESH_BINARY
            )
        return self.imagen_binaria_p2, thresh_val

    def calcular_histograma_p2(self):
        if self.imagen_gris_p2 is None:
            return None, {}

        alto, ancho = self.imagen_gris_p2.shape
        pixels = self.imagen_gris_p2.flatten().astype(np.float64)
        hist, _ = np.histogram(pixels, bins=256, range=(0, 256))
        total = len(pixels)

        # Estadísticas
        media      = float(np.mean(pixels))
        mediana    = float(np.median(pixels))
        moda_val   = int(np.argmax(hist))
        moda_frec  = int(hist[moda_val])
        varianza   = float(np.var(pixels))
        desv_std   = float(np.std(pixels))
        minimo     = int(np.min(pixels))
        maximo     = int(np.max(pixels))

        stats = {
            "Ancho (px)":       ancho,
            "Alto (px)":        alto,
            "Total píxeles":    total,
            "Media":            round(media, 2),
            "Mediana":          round(mediana, 2),
            "Moda":             f"{moda_val}  (frec: {moda_frec})",
            "Varianza":         round(varianza, 2),
            "Desv. Estándar":   round(desv_std, 2),
            "Mínimo":           minimo,
            "Máximo":           maximo,
        }

        # Figura con el histograma de frecuencia
        _, ax1 = plt.subplots(figsize=(8, 4))

        ax1.bar(range(256), hist, color='steelblue', alpha=0.85, width=1)
        ax1.set_xlabel("Intensidad (0-255)")
        ax1.set_ylabel("Frecuencia")
        ax1.set_title("Histograma de Frecuencia")
        ax1.set_xlim(0, 255)
        ax1.axvline(media,    color='red',    linestyle='--', linewidth=1.2, label=f"Media={media:.1f}")
        ax1.axvline(mediana,  color='orange', linestyle='--', linewidth=1.2, label=f"Mediana={mediana:.1f}")
        ax1.axvline(moda_val, color='green',  linestyle='--', linewidth=1.2, label=f"Moda={moda_val}")
        ax1.legend(fontsize=8)

        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches='tight', dpi=100)
        plt.close()
        buf.seek(0)

        file_bytes = np.asarray(bytearray(buf.read()), dtype=np.uint8)
        hist_img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        return hist_img, stats