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

        # Estado P3 - dos imágenes
        self.img1_p3 = None
        self.img2_p3 = None
        self.img1_bin_p3 = None
        self.img2_bin_p3 = None
        self.img1_ruidosa_p3 = None
        self.img2_ruidosa_p3 = None
        # Estado P3 - una imagen
        self.img_una_p3 = None
        self.img_una_gris_p3 = None
        self.img_una_bin_p3 = None
        self.img_una_ruidosa_p3 = None

        # Estado P4 - Morfología Matemática
        self.imagen_p4_gris = None
        self.imagen_p4_bin = None
        self.imagen_p4_trabajo = None   # imagen activa para morfología (gris o binaria)
        self.imagen_p4_resultado = None

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

        umbral_otsu, _ = cv2.threshold(
            self.imagen_gris_p2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

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
            "Umbral Otsu":      int(umbral_otsu),
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

    #                   PRÁCTICA 3

    def cargar_img1_p3(self, ruta):
        self.img1_p3 = cv2.imread(ruta)
        self.img1_ruidosa_p3 = None
        gris = cv2.cvtColor(self.img1_p3, cv2.COLOR_BGR2GRAY)
        _, self.img1_bin_p3 = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return self.img1_bin_p3

    def cargar_img2_p3(self, ruta):
        self.img2_p3 = cv2.imread(ruta)
        self.img2_ruidosa_p3 = None
        gris = cv2.cvtColor(self.img2_p3, cv2.COLOR_BGR2GRAY)
        _, self.img2_bin_p3 = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return self.img2_bin_p3

    def operacion_logica_p3(self, operacion):
        """Aplica operación lógica entre las imágenes binarizadas."""
        if operacion in ("NOT 1", "NOT 2"):
            img = self.img1_bin_p3 if operacion == "NOT 1" else self.img2_bin_p3
            if img is None:
                return None
            return cv2.bitwise_not(img)

        if self.img1_bin_p3 is None or self.img2_bin_p3 is None:
            return None

        h = min(self.img1_bin_p3.shape[0], self.img2_bin_p3.shape[0])
        w = min(self.img1_bin_p3.shape[1], self.img2_bin_p3.shape[1])
        a = cv2.resize(self.img1_bin_p3, (w, h))
        b = cv2.resize(self.img2_bin_p3, (w, h))

        if operacion == "AND":
            return cv2.bitwise_and(a, b)
        elif operacion == "OR":
            return cv2.bitwise_or(a, b)
        elif operacion == "XOR":
            return cv2.bitwise_xor(a, b)
        return None

    def operacion_relacional_p3(self, op, umbral, target=1):
        """Aplica operación relacional a la imagen binarizada (target 1 o 2)."""
        img = self.img1_bin_p3 if target == 1 else self.img2_bin_p3
        if img is None:
            return None
        if op == ">":
            return (img > umbral).astype(np.uint8) * 255
        elif op == "<":
            return (img < umbral).astype(np.uint8) * 255
        elif op == "==":
            return (img == umbral).astype(np.uint8) * 255
        return None

    def _ruido_sal_pimienta(self, img_gris, cantidad):
        """Agrega ruido sal y pimienta a una imagen en escala de grises."""
        ruidosa = img_gris.copy()
        total_px = img_gris.size
        n_ruido = int(total_px * cantidad)

        # Sal (blanco)
        coords_sal = [np.random.randint(0, i, n_ruido // 2) for i in img_gris.shape]
        ruidosa[coords_sal[0], coords_sal[1]] = 255

        # Pimienta (negro)
        coords_pim = [np.random.randint(0, i, n_ruido // 2) for i in img_gris.shape]
        ruidosa[coords_pim[0], coords_pim[1]] = 0

        return ruidosa

    def _ruido_gaussiano(self, img_gris, sigma):
        """Agrega ruido gaussiano a una imagen en escala de grises."""
        ruido = np.random.normal(0, sigma, img_gris.shape).astype(np.float32)
        ruidosa = img_gris.astype(np.float32) + ruido
        ruidosa = np.clip(ruidosa, 0, 255).astype(np.uint8)
        return ruidosa

    def ruido_sp_img1_p3(self, cantidad):
        if self.img1_bin_p3 is None:
            return None
        self.img1_ruidosa_p3 = self._ruido_sal_pimienta(self.img1_bin_p3, cantidad)
        return self.img1_ruidosa_p3

    def ruido_gauss_img1_p3(self, sigma):
        if self.img1_bin_p3 is None:
            return None
        self.img1_ruidosa_p3 = self._ruido_gaussiano(self.img1_bin_p3, sigma)
        return self.img1_ruidosa_p3

    def ruido_sp_img2_p3(self, cantidad):
        if self.img2_bin_p3 is None:
            return None
        self.img2_ruidosa_p3 = self._ruido_sal_pimienta(self.img2_bin_p3, cantidad)
        return self.img2_ruidosa_p3

    def ruido_gauss_img2_p3(self, sigma):
        if self.img2_bin_p3 is None:
            return None
        self.img2_ruidosa_p3 = self._ruido_gaussiano(self.img2_bin_p3, sigma)
        return self.img2_ruidosa_p3

    def etiquetar_dos_filtrada_p3(self, img_bgr, connectivity):
        """Aplica filtro mediana a img_bgr (sin modificar estado) y etiqueta."""
        if img_bgr is None:
            return None, None, 0
        gris = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        filtrada = cv2.medianBlur(gris, 3)
        return self.etiquetar_p3(filtrada, connectivity)

    def etiquetar_p3(self, img_bin_o_gris, connectivity):
        """
        Umbraliza a 127, ejecuta connectedComponents con la conectividad dada.
        Retorna (colored_labels_BGR, contoured_BGR, count).
        Optimizado: colorización vectorizada y un único findContours.
        """
        if img_bin_o_gris is None:
            return None, None, 0

        if len(img_bin_o_gris.shape) == 3:
            gris = cv2.cvtColor(img_bin_o_gris, cv2.COLOR_BGR2GRAY)
        else:
            gris = img_bin_o_gris.copy()

        _, binaria = cv2.threshold(gris, 127, 255, cv2.THRESH_BINARY)
        binaria = cv2.bitwise_not(binaria)   # objetos en blanco, fondo negro
        num_labels, labels = cv2.connectedComponents(binaria, connectivity=connectivity)
        count = num_labels - 1

        # Colorización vectorizada con numpy fancy indexing (sin loop por etiqueta)
        np.random.seed(42)
        colors = np.random.randint(60, 240, (num_labels, 3), dtype=np.uint8)
        colors[0] = [0, 0, 180]  # fondo rojo (BGR)
        colored = colors[labels]  # shape (H, W, 3) en un solo paso

        # Contornos: un único findContours sobre la imagen binaria completa
        contoured = cv2.cvtColor(binaria, cv2.COLOR_GRAY2BGR)
        contours, _ = cv2.findContours(binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for i, cnt in enumerate(contours):
            cv2.drawContours(contoured, [cnt], -1, (0, 200, 0), 1)
            x, y, _, _ = cv2.boundingRect(cnt)
            cv2.putText(contoured, str(i + 1), (x, max(y - 3, 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

        return colored, contoured, count

    # --- P3 Una Imagen ---

    def cargar_img_una_p3(self, ruta):
        self.img_una_p3 = cv2.imread(ruta)
        self.img_una_gris_p3 = None
        self.img_una_bin_p3 = None
        self.img_una_ruidosa_p3 = None
        return self.img_una_p3

    def convertir_gris_una_p3(self):
        if self.img_una_p3 is None:
            return None
        self.img_una_gris_p3 = cv2.cvtColor(self.img_una_p3, cv2.COLOR_BGR2GRAY)
        return self.img_una_gris_p3

    def binarizar_una_p3(self, umbral=None):
        """None = Otsu, int = umbral fijo. Retorna (img, thresh_val)."""
        if self.img_una_gris_p3 is None:
            return None, None
        if umbral is None:
            thresh_val, self.img_una_bin_p3 = cv2.threshold(
                self.img_una_gris_p3, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )
        else:
            thresh_val, self.img_una_bin_p3 = cv2.threshold(
                self.img_una_gris_p3, umbral, 255, cv2.THRESH_BINARY
            )
        return self.img_una_bin_p3, thresh_val

    def not_una_p3(self):
        """Invierte img_una_bin_p3 (NOT lógico) y actualiza el estado."""
        if self.img_una_bin_p3 is None:
            return None
        self.img_una_bin_p3 = cv2.bitwise_not(self.img_una_bin_p3)
        self.img_una_ruidosa_p3 = None  # el ruido anterior ya no aplica
        return self.img_una_bin_p3

    def ruido_sp_una_p3(self, cantidad):
        """Aplica ruido S&P a img_una_bin_p3. Guarda en img_una_ruidosa_p3."""
        if self.img_una_bin_p3 is None:
            return None
        self.img_una_ruidosa_p3 = self._ruido_sal_pimienta(self.img_una_bin_p3, cantidad)
        return self.img_una_ruidosa_p3

    def ruido_gauss_una_p3(self, sigma):
        """Aplica ruido gaussiano a img_una_gris_p3. Guarda en img_una_ruidosa_p3."""
        if self.img_una_gris_p3 is None:
            return None
        self.img_una_ruidosa_p3 = self._ruido_gaussiano(self.img_una_gris_p3, sigma)
        return self.img_una_ruidosa_p3

    def etiquetar_filtrada_p3(self, connectivity):
        """Aplica filtro mediana 3x3 a la imagen ruidosa (sin modificar estado) y etiqueta."""
        if self.img_una_ruidosa_p3 is None:
            return None, None, 0
        filtrada = cv2.medianBlur(self.img_una_ruidosa_p3, 3)
        return self.etiquetar_p3(filtrada, connectivity)

    #                   PRÁCTICA 4

    def cargar_imagen_p4(self, ruta):
        img = cv2.imread(ruta)
        if img is None:
            return None
        self.imagen_p4_gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.imagen_p4_bin = None
        self.imagen_p4_trabajo = self.imagen_p4_gris
        self.imagen_p4_resultado = None
        return self.imagen_p4_gris

    def binarizar_p4(self, umbral=None):
        """None = Otsu, int = umbral fijo. Retorna (img_bin, thresh_val)."""
        if self.imagen_p4_gris is None:
            return None, None
        if umbral is None:
            thresh_val, self.imagen_p4_bin = cv2.threshold(
                self.imagen_p4_gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )
        else:
            thresh_val, self.imagen_p4_bin = cv2.threshold(
                self.imagen_p4_gris, umbral, 255, cv2.THRESH_BINARY
            )
        self.imagen_p4_trabajo = self.imagen_p4_bin
        self.imagen_p4_resultado = None
        return self.imagen_p4_bin, thresh_val

    def morfologia_p4(self, operacion, kernel_size, iteraciones):
        if self.imagen_p4_trabajo is None:
            return None
        k = max(1, int(kernel_size))
        it = max(1, int(iteraciones))
        kernel = np.ones((k, k), np.uint8)
        if operacion == "Erosión":
            resultado = cv2.erode(self.imagen_p4_trabajo, kernel, iterations=it)
        elif operacion == "Dilatación":
            resultado = cv2.dilate(self.imagen_p4_trabajo, kernel, iterations=it)
        elif operacion == "Apertura":
            resultado = cv2.morphologyEx(self.imagen_p4_trabajo, cv2.MORPH_OPEN, kernel, iterations=it)
        elif operacion == "Cierre":
            resultado = cv2.morphologyEx(self.imagen_p4_trabajo, cv2.MORPH_CLOSE, kernel, iterations=it)
        else:
            return None
        self.imagen_p4_resultado = resultado
        return resultado
