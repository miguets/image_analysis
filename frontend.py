import tkinter as tk
from tkinter import filedialog, ttk
import cv2
from PIL import Image, ImageTk

class InterfazApp:
    def __init__(self, root, backend):
        self.root = root
        self.backend = backend
        self.root.title("Prácticas de Visión por Computadora")
        self.root.geometry("1100x650")

        style = ttk.Style()
        style.theme_use('clam')

        # --- Barra Superior (Menú de Prácticas) ---
        self.frame_top = ttk.Frame(self.root, padding="10")
        self.frame_top.pack(side="top", fill="x")

        ttk.Label(self.frame_top, text="Selecciona la Práctica:", font=("Arial", 11, "bold")).pack(side="left", padx=5)

        self.combo_practicas = ttk.Combobox(self.frame_top, state="readonly", width=30)
        self.combo_practicas['values'] = ("1. Mapas de Calor", "2. Modelos de Color", "3. Práctica 3 (Próximamente)")
        self.combo_practicas.set("1. Mapas de Calor")
        self.combo_practicas.pack(side="left", padx=10)
        self.combo_practicas.bind("<<ComboboxSelected>>", self.cambiar_practica)

        ttk.Separator(self.root, orient='horizontal').pack(fill='x', pady=5)

        self.workspace = ttk.Frame(self.root, padding="10")
        self.workspace.pack(fill="both", expand=True)

        self.cargar_interfaz_mapas()

    def cambiar_practica(self, event=None):
        seleccion = self.combo_practicas.get()
        for widget in self.workspace.winfo_children():
            widget.destroy()

        if "Mapas de Calor" in seleccion:
            self.root.geometry("1100x650")
            self.cargar_interfaz_mapas()
        elif "Modelos de Color" in seleccion:
            self.root.geometry("1150x780")
            self.cargar_interfaz_practica2()
        else:
            ttk.Label(self.workspace, text=f"La {seleccion} aún no está implementada.", font=("Arial", 14)).pack(pady=100)

    # ==================== PRÁCTICA 1 ====================

    def cargar_interfaz_mapas(self):
        frame_controles = ttk.Frame(self.workspace)
        frame_controles.pack(fill="x", pady=10)

        ttk.Button(frame_controles, text="Subir Imagen", command=self.evento_cargar_imagen).grid(row=0, column=0, padx=20)
        ttk.Label(frame_controles, text="Mapa de Color:").grid(row=0, column=1, padx=5)
        self.combo_mapas = ttk.Combobox(frame_controles, values=self.backend.obtener_nombres_mapas(), state="readonly")
        self.combo_mapas.set("Grises")
        self.combo_mapas.grid(row=0, column=2, padx=5)
        ttk.Button(frame_controles, text="Aplicar mapa", command=self.evento_aplicar_mapa).grid(row=0, column=3, padx=20)

        frame_imagenes = ttk.Frame(self.workspace)
        frame_imagenes.pack(fill="both", expand=True, pady=10)
        for i in range(3):
            frame_imagenes.columnconfigure(i, weight=1)

        ttk.Label(frame_imagenes, text="Original",      font=("Arial", 10, "bold")).grid(row=0, column=0)
        ttk.Label(frame_imagenes, text="Mapa Anterior", font=("Arial", 10, "bold")).grid(row=0, column=1)
        ttk.Label(frame_imagenes, text="Mapa Nuevo",    font=("Arial", 10, "bold")).grid(row=0, column=2)

        self.panel_original = tk.Label(frame_imagenes, bg="#e0e0e0", relief="sunken", width=42, height=20)
        self.panel_original.grid(row=1, column=0, padx=10, pady=10)
        self.panel_anterior = tk.Label(frame_imagenes, bg="#e0e0e0", relief="sunken", width=42, height=20)
        self.panel_anterior.grid(row=1, column=1, padx=10, pady=10)
        self.panel_nuevo = tk.Label(frame_imagenes, bg="#e0e0e0", relief="sunken", width=42, height=20)
        self.panel_nuevo.grid(row=1, column=2, padx=10, pady=10)

    def mostrar_en_panel(self, panel, img_cv2):
        if img_cv2 is None:
            return
        img = cv2.resize(img_cv2, (300, 300))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img)
        img_tk = ImageTk.PhotoImage(img_pil)
        panel.config(image=img_tk, width=300, height=300)
        panel.image = img_tk

    def evento_cargar_imagen(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.jpeg *.png")])
        if ruta:
            img = self.backend.cargar_imagen(ruta)
            self.mostrar_en_panel(self.panel_original, img)
            self.panel_anterior.config(image='')
            self.panel_nuevo.config(image='')

    def evento_aplicar_mapa(self):
        mapa_seleccionado = self.combo_mapas.get()
        exito = self.backend.aplicar_mapa_color(mapa_seleccionado)
        if exito:
            self.mostrar_en_panel(self.panel_anterior, self.backend.imagen_anterior)
            self.mostrar_en_panel(self.panel_nuevo, self.backend.imagen_nueva)

    # ==================== PRÁCTICA 2 ====================

    def cargar_interfaz_practica2(self):
        # --- Barra de controles ---
        frame_ctrl = ttk.Frame(self.workspace)
        frame_ctrl.pack(fill="x", pady=5, padx=5)

        ttk.Button(frame_ctrl, text="Subir Imagen", command=self._p2_cargar_imagen).pack(side="left", padx=4)
        ttk.Separator(frame_ctrl, orient='vertical').pack(side="left", fill='y', padx=8)

        ttk.Label(frame_ctrl, text="Modelo:").pack(side="left")
        self.combo_modelo_p2 = ttk.Combobox(frame_ctrl, values=["RGB", "CMY", "HSV"], state="readonly", width=6)
        self.combo_modelo_p2.set("RGB")
        self.combo_modelo_p2.pack(side="left", padx=4)
        ttk.Button(frame_ctrl, text="Separar Canales", command=self._p2_separar).pack(side="left", padx=4)
        ttk.Separator(frame_ctrl, orient='vertical').pack(side="left", fill='y', padx=8)

        ttk.Button(frame_ctrl, text="Convertir a Grises", command=self._p2_grises).pack(side="left", padx=4)
        ttk.Separator(frame_ctrl, orient='vertical').pack(side="left", fill='y', padx=8)

        ttk.Label(frame_ctrl, text="Umbral (0-255):").pack(side="left")
        self.entry_umbral_p2 = ttk.Entry(frame_ctrl, width=5)
        self.entry_umbral_p2.insert(0, "128")
        self.entry_umbral_p2.pack(side="left", padx=4)
        ttk.Button(frame_ctrl, text="Binarizar Fijo",  command=self._p2_binarizar_fijo).pack(side="left", padx=4)
        ttk.Button(frame_ctrl, text="Binarizar Otsu",  command=self._p2_binarizar_otsu).pack(side="left", padx=4)
        ttk.Separator(frame_ctrl, orient='vertical').pack(side="left", fill='y', padx=8)

        ttk.Button(frame_ctrl, text="Ver Histograma", command=self._p2_histograma).pack(side="left", padx=4)

        # --- Sección: separación de canales ---
        frame_canales = ttk.LabelFrame(self.workspace, text="Separación de Canales de Color")
        frame_canales.pack(fill="x", padx=5, pady=5)
        for i in range(4):
            frame_canales.columnconfigure(i, weight=1)

        ttk.Label(frame_canales, text="Original", font=("Arial", 9, "bold")).grid(row=0, column=0, pady=2)
        self.lbl_p2_c1 = ttk.Label(frame_canales, text="Canal 1", font=("Arial", 9, "bold"))
        self.lbl_p2_c1.grid(row=0, column=1, pady=2)
        self.lbl_p2_c2 = ttk.Label(frame_canales, text="Canal 2", font=("Arial", 9, "bold"))
        self.lbl_p2_c2.grid(row=0, column=2, pady=2)
        self.lbl_p2_c3 = ttk.Label(frame_canales, text="Canal 3", font=("Arial", 9, "bold"))
        self.lbl_p2_c3.grid(row=0, column=3, pady=2)

        self.panel_p2_orig = tk.Label(frame_canales, bg="#e0e0e0", relief="sunken", width=28, height=12)
        self.panel_p2_orig.grid(row=1, column=0, padx=6, pady=5)
        self.panel_p2_c1 = tk.Label(frame_canales, bg="#e0e0e0", relief="sunken", width=28, height=12)
        self.panel_p2_c1.grid(row=1, column=1, padx=6, pady=5)
        self.panel_p2_c2 = tk.Label(frame_canales, bg="#e0e0e0", relief="sunken", width=28, height=12)
        self.panel_p2_c2.grid(row=1, column=2, padx=6, pady=5)
        self.panel_p2_c3 = tk.Label(frame_canales, bg="#e0e0e0", relief="sunken", width=28, height=12)
        self.panel_p2_c3.grid(row=1, column=3, padx=6, pady=5)

        # --- Sección: conversión y binarización ---
        frame_proc = ttk.LabelFrame(self.workspace, text="Conversión y Binarización")
        frame_proc.pack(fill="x", padx=5, pady=5)
        for i in range(2):
            frame_proc.columnconfigure(i, weight=1)

        ttk.Label(frame_proc, text="Escala de Grises",  font=("Arial", 9, "bold")).grid(row=0, column=0, pady=2)
        ttk.Label(frame_proc, text="Imagen Binarizada", font=("Arial", 9, "bold")).grid(row=0, column=1, pady=2)

        self.panel_p2_gris = tk.Label(frame_proc, bg="#e0e0e0", relief="sunken", width=42, height=16)
        self.panel_p2_gris.grid(row=1, column=0, padx=10, pady=5)
        self.panel_p2_bin  = tk.Label(frame_proc, bg="#e0e0e0", relief="sunken", width=42, height=16)
        self.panel_p2_bin.grid(row=1, column=1, padx=10, pady=5)

        # Barra de estado
        self.lbl_p2_status = ttk.Label(self.workspace, text="Carga una imagen para comenzar.",
                                        font=("Arial", 9), foreground="gray")
        self.lbl_p2_status.pack(pady=3)

    def _p2_mostrar(self, panel, img_cv2, size=200):
        """Muestra una imagen (BGR o grayscale) en un panel tkinter redimensionada a `size` px."""
        if img_cv2 is None:
            return
        img = cv2.resize(img_cv2, (size, size))
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img)
        img_tk  = ImageTk.PhotoImage(img_pil)
        panel.config(image=img_tk, width=size, height=size)
        panel.image = img_tk

    def _p2_cargar_imagen(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.jpeg *.png")])
        if ruta:
            img = self.backend.cargar_imagen_p2(ruta)
            self._p2_mostrar(self.panel_p2_orig, img, 200)
            for panel in [self.panel_p2_c1, self.panel_p2_c2, self.panel_p2_c3,
                          self.panel_p2_gris, self.panel_p2_bin]:
                panel.config(image='')
            self.lbl_p2_status.config(
                text="Imagen cargada. Selecciona un modelo y separa los canales.", foreground="blue")

    def _p2_separar(self):
        modelo = self.combo_modelo_p2.get()
        componentes = self.backend.separar_componentes_p2(modelo)
        if not componentes:
            self.lbl_p2_status.config(text="Primero carga una imagen.", foreground="red")
            return

        nombres = {
            "RGB": ["Canal R (Rojo)",    "Canal G (Verde)",      "Canal B (Azul)"],
            "CMY": ["Canal C (Cian)",    "Canal M (Magenta)",    "Canal Y (Amarillo)"],
            "HSV": ["Canal H (Matiz)",   "Canal S (Saturación)", "Canal V (Brillo)"],
        }
        titulos = nombres.get(modelo, ["Canal 1", "Canal 2", "Canal 3"])
        self.lbl_p2_c1.config(text=titulos[0])
        self.lbl_p2_c2.config(text=titulos[1])
        self.lbl_p2_c3.config(text=titulos[2])

        for panel, (img, _) in zip([self.panel_p2_c1, self.panel_p2_c2, self.panel_p2_c3], componentes):
            self._p2_mostrar(panel, img, 200)
        self.lbl_p2_status.config(
            text=f"Canales del modelo {modelo} separados correctamente.", foreground="green")

    def _p2_grises(self):
        img = self.backend.convertir_grises_p2()
        if img is None:
            self.lbl_p2_status.config(text="Primero carga una imagen.", foreground="red")
            return
        self._p2_mostrar(self.panel_p2_gris, img, 260)
        self.lbl_p2_status.config(text="Imagen convertida a escala de grises.", foreground="green")

    def _p2_binarizar_fijo(self):
        try:
            umbral = max(0, min(255, int(self.entry_umbral_p2.get())))
        except ValueError:
            umbral = 128
        img, thresh = self.backend.binarizar_p2(umbral)
        if img is None:
            self.lbl_p2_status.config(text="Primero convierte la imagen a grises.", foreground="red")
            return
        self._p2_mostrar(self.panel_p2_bin, img, 260)
        self.lbl_p2_status.config(
            text=f"Binarización fija aplicada — umbral = {int(thresh)}.", foreground="green")

    def _p2_binarizar_otsu(self):
        img, thresh = self.backend.binarizar_p2(None)
        if img is None:
            self.lbl_p2_status.config(text="Primero convierte la imagen a grises.", foreground="red")
            return
        self._p2_mostrar(self.panel_p2_bin, img, 260)
        self.lbl_p2_status.config(
            text=f"Binarización Otsu — umbral automático = {int(thresh)}.", foreground="green")

    def _p2_histograma(self):
        hist_img, stats = self.backend.calcular_histograma_p2()
        if hist_img is None:
            self.lbl_p2_status.config(text="Primero convierte la imagen a grises.", foreground="red")
            return

        popup = tk.Toplevel(self.root)
        popup.title("Histograma de Intensidad — Estadísticas")
        popup.resizable(False, False)

        # Redimensionar la imagen del histograma para que quepa en el popup
        h_orig, w_orig = hist_img.shape[:2]
        target_w = 700
        target_h = int(h_orig * target_w / w_orig)
        img_rgb = cv2.cvtColor(hist_img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb).resize((target_w, target_h), Image.LANCZOS)
        img_tk  = ImageTk.PhotoImage(img_pil)

        popup.geometry(f"{target_w + 360}x{max(target_h + 50, 420)}")

        lbl_img = tk.Label(popup, image=img_tk)
        lbl_img.image = img_tk
        lbl_img.pack(side="left", padx=10, pady=10)

        # Panel de estadísticas
        frame_stats = ttk.LabelFrame(popup, text="Estadísticas de Intensidad", padding=12)
        frame_stats.pack(side="left", fill="y", padx=10, pady=10)

        for i, (key, val) in enumerate(stats.items()):
            ttk.Label(frame_stats, text=f"{key}:", font=("Arial", 10, "bold"),
                      anchor="e", width=20).grid(row=i, column=0, sticky="e", pady=5)
            ttk.Label(frame_stats, text=str(val), font=("Arial", 10),
                      anchor="w", width=22).grid(row=i, column=1, sticky="w", padx=10, pady=5)

        ttk.Button(popup, text="Cerrar", command=popup.destroy).pack(side="bottom", pady=8)
