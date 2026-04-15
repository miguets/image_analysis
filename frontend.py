import tkinter as tk
from tkinter import filedialog, ttk
import cv2
from PIL import Image, ImageTk

class InterfazApp:
    def __init__(self, root, backend):
        self.root = root
        self.backend = backend
        self._panel_imgs = {}   # id(panel) → img cv2 original para guardar
        self.root.title("Prácticas de Visión por Computadora")
        self.root.geometry("1100x650")

        style = ttk.Style()
        style.theme_use('clam')

        # --- Barra Superior (Menú de Prácticas) ---
        self.frame_top = ttk.Frame(self.root, padding="10")
        self.frame_top.pack(side="top", fill="x")

        ttk.Label(self.frame_top, text="Selecciona la Práctica:", font=("Arial", 11, "bold")).pack(side="left", padx=5)

        self.combo_practicas = ttk.Combobox(self.frame_top, state="readonly", width=30)
        self.combo_practicas['values'] = ("1. Mapas de Calor", "2. Modelos de Color", "3. Operaciones y Etiquetado", "4. Morfología Matemática")
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
        elif "Operaciones" in seleccion:
            self.root.geometry("1200x1000")
            self.cargar_interfaz_practica3()
        elif "Morfología" in seleccion:
            self.root.geometry("1100x700")
            self.cargar_interfaz_practica4()
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
        ttk.Button(frame_controles, text="Guardar Mapa Nuevo", command=self.evento_guardar_mapa).grid(row=0, column=4, padx=10)

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

    def evento_guardar_mapa(self):
        if self.backend.imagen_nueva is None:
            return
        ruta = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("Todos", "*.*")]
        )
        if ruta:
            cv2.imwrite(ruta, self.backend.imagen_nueva)

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

        ttk.Button(frame_canales, text="Guardar Canal 1",
                   command=lambda: self._p2_guardar_canal(0)).grid(row=2, column=1, pady=4)
        ttk.Button(frame_canales, text="Guardar Canal 2",
                   command=lambda: self._p2_guardar_canal(1)).grid(row=2, column=2, pady=4)
        ttk.Button(frame_canales, text="Guardar Canal 3",
                   command=lambda: self._p2_guardar_canal(2)).grid(row=2, column=3, pady=4)

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

        ttk.Button(frame_proc, text="Guardar Grises",
                   command=self._p2_guardar_gris).grid(row=2, column=0, pady=4)
        ttk.Button(frame_proc, text="Guardar Binarizada",
                   command=self._p2_guardar_bin).grid(row=2, column=1, pady=4)

        # Barra de estado
        self.lbl_p2_status = ttk.Label(self.workspace, text="Carga una imagen para comenzar.",
                                        font=("Arial", 9), foreground="gray")
        self.lbl_p2_status.pack(pady=3)

    def _p2_mostrar(self, panel, img_cv2, size=200):
        """Muestra una imagen (BGR o grayscale) en un panel tkinter redimensionada a `size` px."""
        if img_cv2 is None:
            return
        self._panel_imgs[id(panel)] = img_cv2
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

    # ==================== PRÁCTICA 3 ====================

    def _p2_guardar_canal(self, indice):
        if not self.backend.componentes_p2 or indice >= len(self.backend.componentes_p2):
            return
        img, _ = self.backend.componentes_p2[indice]
        ruta = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("Todos", "*.*")]
        )
        if ruta:
            cv2.imwrite(ruta, img)

    def _p2_guardar_gris(self):
        if self.backend.imagen_gris_p2 is None:
            return
        ruta = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("Todos", "*.*")]
        )
        if ruta:
            cv2.imwrite(ruta, self.backend.imagen_gris_p2)

    def _p2_guardar_bin(self):
        if self.backend.imagen_binaria_p2 is None:
            return
        ruta = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("Todos", "*.*")]
        )
        if ruta:
            cv2.imwrite(ruta, self.backend.imagen_binaria_p2)

    # ---- helpers de guardado por clic derecho (P3) ----

    def _bind_guardar_panel(self, panel):
        """Vincula clic derecho en un panel para guardar la imagen almacenada en _panel_imgs."""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Guardar imagen",
                         command=lambda: self._guardar_desde_panel(panel))
        panel.bind("<Button-3>", lambda e: menu.tk_popup(e.x_root, e.y_root))

    def _guardar_desde_panel(self, panel):
        img = self._panel_imgs.get(id(panel))
        if img is None:
            return
        ruta = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("Todos", "*.*")]
        )
        if ruta:
            cv2.imwrite(ruta, img)

    def cargar_interfaz_practica3(self):
        # --- Selector de modo ---
        frame_modo = ttk.Frame(self.workspace)
        frame_modo.pack(fill="x", pady=5, padx=5)

        ttk.Label(frame_modo, text="Modo:", font=("Arial", 10, "bold")).pack(side="left", padx=5)

        self._p3_modo_var = tk.StringVar(value="dos")
        ttk.Radiobutton(frame_modo, text="Dos Imágenes",
                        variable=self._p3_modo_var, value="dos",
                        command=self._p3_cambiar_modo).pack(side="left", padx=10)
        ttk.Radiobutton(frame_modo, text="Una Imagen",
                        variable=self._p3_modo_var, value="una",
                        command=self._p3_cambiar_modo).pack(side="left", padx=10)

        ttk.Separator(self.workspace, orient='horizontal').pack(fill='x', pady=4)

        # --- Contenedor de contenido (se reconstruye al cambiar modo) ---
        self._frame_p3_contenido = ttk.Frame(self.workspace)
        self._frame_p3_contenido.pack(fill="both", expand=True)

        self._p3_construir_dos_imagenes()

    def _p3_cambiar_modo(self):
        for widget in self._frame_p3_contenido.winfo_children():
            widget.destroy()
        if self._p3_modo_var.get() == "dos":
            self._p3_construir_dos_imagenes()
        else:
            self._p3_construir_una_imagen()

    # ---------- Dos Imágenes (Parte A y B) ----------

    def _p3_construir_dos_imagenes(self):
        parent = self._frame_p3_contenido

        # --- Fila 1: cargar + op. lógica ---
        ctrl1 = ttk.Frame(parent)
        ctrl1.pack(fill="x", pady=3, padx=5)

        ttk.Button(ctrl1, text="Cargar Imagen 1", command=self._p3_cargar_img1).pack(side="left", padx=4)
        ttk.Button(ctrl1, text="Cargar Imagen 2", command=self._p3_cargar_img2).pack(side="left", padx=4)
        ttk.Separator(ctrl1, orient='vertical').pack(side="left", fill='y', padx=8)

        ttk.Label(ctrl1, text="Op. Lógica:").pack(side="left")
        self._p3_combo_logica = ttk.Combobox(ctrl1, values=["AND", "OR", "XOR", "NOT 1", "NOT 2"],
                                              state="readonly", width=8)
        self._p3_combo_logica.set("AND")
        self._p3_combo_logica.pack(side="left", padx=4)
        ttk.Button(ctrl1, text="Aplicar", command=self._p3_op_logica).pack(side="left", padx=4)

        # --- Fila 2: ruido + etiquetar ---
        ctrl2 = ttk.Frame(parent)
        ctrl2.pack(fill="x", pady=3, padx=5)

        ttk.Label(ctrl2, text="S&P cant:").pack(side="left")
        self._p3_entry_sp_dos = ttk.Entry(ctrl2, width=5)
        self._p3_entry_sp_dos.insert(0, "0.05")
        self._p3_entry_sp_dos.pack(side="left", padx=2)
        ttk.Button(ctrl2, text="Aplicar Img1", command=self._p3_ruido_sp_dos).pack(side="left", padx=2)
        ttk.Button(ctrl2, text="Aplicar Img2", command=self._p3_ruido_sp_img2).pack(side="left", padx=2)
        ttk.Separator(ctrl2, orient='vertical').pack(side="left", fill='y', padx=8)

        ttk.Label(ctrl2, text="Gauss σ:").pack(side="left")
        self._p3_entry_gauss_dos = ttk.Entry(ctrl2, width=5)
        self._p3_entry_gauss_dos.insert(0, "25")
        self._p3_entry_gauss_dos.pack(side="left", padx=2)
        ttk.Button(ctrl2, text="Aplicar Img1", command=self._p3_ruido_gauss_dos).pack(side="left", padx=2)
        ttk.Button(ctrl2, text="Aplicar Img2", command=self._p3_ruido_gauss_img2).pack(side="left", padx=2)
        ttk.Separator(ctrl2, orient='vertical').pack(side="left", fill='y', padx=8)

        ttk.Button(ctrl2, text="Etiquetar Img1", command=self._p3_etiquetar_dos_img1).pack(side="left", padx=4)
        ttk.Button(ctrl2, text="Etiquetar Img2", command=self._p3_etiquetar_dos_img2).pack(side="left", padx=4)

        # --- Imágenes (binarizadas al cargar) + resultado lógico ---
        frame_imgs = ttk.LabelFrame(parent, text="Imágenes")
        frame_imgs.pack(fill="x", padx=5, pady=4)
        for i in range(3):
            frame_imgs.columnconfigure(i, weight=1)

        ttk.Label(frame_imgs, text="Imagen 1 (binarizada)", font=("Arial", 9, "bold")).grid(row=0, column=0, pady=2)
        ttk.Label(frame_imgs, text="Imagen 2 (binarizada)", font=("Arial", 9, "bold")).grid(row=0, column=1, pady=2)
        ttk.Label(frame_imgs, text="Resultado Lógico",       font=("Arial", 9, "bold")).grid(row=0, column=2, pady=2)

        self._p3_panel_img1   = tk.Label(frame_imgs, bg="#e0e0e0", relief="sunken", width=30, height=13)
        self._p3_panel_img1.grid(row=1, column=0, padx=8, pady=4)
        self._p3_panel_img2   = tk.Label(frame_imgs, bg="#e0e0e0", relief="sunken", width=30, height=13)
        self._p3_panel_img2.grid(row=1, column=1, padx=8, pady=4)
        self._p3_panel_logica = tk.Label(frame_imgs, bg="#e0e0e0", relief="sunken", width=30, height=13)
        self._p3_panel_logica.grid(row=1, column=2, padx=8, pady=4)

        # --- Procesamiento Imagen 1: Con Ruido | V4 ruido | V8 ruido | V4 binarizada | V8 binarizada ---
        frame_p1 = ttk.LabelFrame(parent, text="Procesamiento Imagen 1")
        frame_p1.pack(fill="x", padx=5, pady=4)
        for i in range(5):
            frame_p1.columnconfigure(i, weight=1)

        self._lbl_dos_r1_c  = ttk.Label(frame_p1, text="Con Ruido",           font=("Arial", 8, "bold"))
        self._lbl_dos_r1_v4 = ttk.Label(frame_p1, text="Etiq. V4\n(ruido)",   font=("Arial", 8, "bold"))
        self._lbl_dos_r1_v8 = ttk.Label(frame_p1, text="Etiq. V8\n(ruido)",   font=("Arial", 8, "bold"))
        self._lbl_dos_b1_v4 = ttk.Label(frame_p1, text="Etiq. V4\n(binaria)", font=("Arial", 8, "bold"))
        self._lbl_dos_b1_v8 = ttk.Label(frame_p1, text="Etiq. V8\n(binaria)", font=("Arial", 8, "bold"))
        for col, lbl in enumerate([self._lbl_dos_r1_c, self._lbl_dos_r1_v4, self._lbl_dos_r1_v8,
                                    self._lbl_dos_b1_v4, self._lbl_dos_b1_v8]):
            lbl.grid(row=0, column=col, pady=2)

        self._p3_panel_ruido1         = tk.Label(frame_p1, bg="#e0e0e0", relief="sunken", width=20, height=11)
        self._p3_panel_ruido1.grid(row=1, column=0, padx=4, pady=4)
        self._p3_panel_etiq_v4_img1   = tk.Label(frame_p1, bg="#e0e0e0", relief="sunken", width=20, height=11)
        self._p3_panel_etiq_v4_img1.grid(row=1, column=1, padx=4, pady=4)
        self._p3_panel_etiq_v8_img1   = tk.Label(frame_p1, bg="#e0e0e0", relief="sunken", width=20, height=11)
        self._p3_panel_etiq_v8_img1.grid(row=1, column=2, padx=4, pady=4)
        self._p3_panel_etiq_v4_img1_f = tk.Label(frame_p1, bg="#e0e0e0", relief="sunken", width=20, height=11)
        self._p3_panel_etiq_v4_img1_f.grid(row=1, column=3, padx=4, pady=4)
        self._p3_panel_etiq_v8_img1_f = tk.Label(frame_p1, bg="#e0e0e0", relief="sunken", width=20, height=11)
        self._p3_panel_etiq_v8_img1_f.grid(row=1, column=4, padx=4, pady=4)

        # --- Procesamiento Imagen 2 ---
        frame_p2 = ttk.LabelFrame(parent, text="Procesamiento Imagen 2")
        frame_p2.pack(fill="x", padx=5, pady=4)
        for i in range(5):
            frame_p2.columnconfigure(i, weight=1)

        self._lbl_dos_r2_c  = ttk.Label(frame_p2, text="Con Ruido",           font=("Arial", 8, "bold"))
        self._lbl_dos_r2_v4 = ttk.Label(frame_p2, text="Etiq. V4\n(ruido)",   font=("Arial", 8, "bold"))
        self._lbl_dos_r2_v8 = ttk.Label(frame_p2, text="Etiq. V8\n(ruido)",   font=("Arial", 8, "bold"))
        self._lbl_dos_b2_v4 = ttk.Label(frame_p2, text="Etiq. V4\n(binaria)", font=("Arial", 8, "bold"))
        self._lbl_dos_b2_v8 = ttk.Label(frame_p2, text="Etiq. V8\n(binaria)", font=("Arial", 8, "bold"))
        for col, lbl in enumerate([self._lbl_dos_r2_c, self._lbl_dos_r2_v4, self._lbl_dos_r2_v8,
                                    self._lbl_dos_b2_v4, self._lbl_dos_b2_v8]):
            lbl.grid(row=0, column=col, pady=2)

        self._p3_panel_ruido2         = tk.Label(frame_p2, bg="#e0e0e0", relief="sunken", width=20, height=11)
        self._p3_panel_ruido2.grid(row=1, column=0, padx=4, pady=4)
        self._p3_panel_etiq_v4_img2   = tk.Label(frame_p2, bg="#e0e0e0", relief="sunken", width=20, height=11)
        self._p3_panel_etiq_v4_img2.grid(row=1, column=1, padx=4, pady=4)
        self._p3_panel_etiq_v8_img2   = tk.Label(frame_p2, bg="#e0e0e0", relief="sunken", width=20, height=11)
        self._p3_panel_etiq_v8_img2.grid(row=1, column=2, padx=4, pady=4)
        self._p3_panel_etiq_v4_img2_f = tk.Label(frame_p2, bg="#e0e0e0", relief="sunken", width=20, height=11)
        self._p3_panel_etiq_v4_img2_f.grid(row=1, column=3, padx=4, pady=4)
        self._p3_panel_etiq_v8_img2_f = tk.Label(frame_p2, bg="#e0e0e0", relief="sunken", width=20, height=11)
        self._p3_panel_etiq_v8_img2_f.grid(row=1, column=4, padx=4, pady=4)

        # --- Resultado Relacional (al fondo) ---
        frame_rel = ttk.LabelFrame(parent, text="Resultado Relacional")
        frame_rel.pack(fill="x", padx=5, pady=4)
        frame_rel.columnconfigure(0, weight=0)
        frame_rel.columnconfigure(1, weight=1)

        ctrl_rel = ttk.Frame(frame_rel)
        ctrl_rel.grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=4)

        ttk.Label(ctrl_rel, text="Aplicar a:").pack(side="left")
        self._p3_combo_rel_target = ttk.Combobox(ctrl_rel, values=["Imagen 1", "Imagen 2"],
                                                   state="readonly", width=10)
        self._p3_combo_rel_target.set("Imagen 1")
        self._p3_combo_rel_target.pack(side="left", padx=4)
        ttk.Label(ctrl_rel, text="Op.:").pack(side="left")
        self._p3_combo_relacional = ttk.Combobox(ctrl_rel, values=[">", "<", "=="], state="readonly", width=4)
        self._p3_combo_relacional.set(">")
        self._p3_combo_relacional.pack(side="left", padx=2)
        ttk.Label(ctrl_rel, text="Umbral:").pack(side="left")
        self._p3_entry_umbral_rel = ttk.Entry(ctrl_rel, width=5)
        self._p3_entry_umbral_rel.insert(0, "128")
        self._p3_entry_umbral_rel.pack(side="left", padx=2)
        ttk.Button(ctrl_rel, text="Aplicar", command=self._p3_op_relacional).pack(side="left", padx=6)

        self._p3_panel_relacional = tk.Label(frame_rel, bg="#e0e0e0", relief="sunken", width=30, height=12)
        self._p3_panel_relacional.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        # Clic derecho para guardar en todos los paneles
        for _panel in [self._p3_panel_img1, self._p3_panel_img2, self._p3_panel_logica,
                       self._p3_panel_ruido1, self._p3_panel_ruido2,
                       self._p3_panel_etiq_v4_img1, self._p3_panel_etiq_v8_img1,
                       self._p3_panel_etiq_v4_img1_f, self._p3_panel_etiq_v8_img1_f,
                       self._p3_panel_etiq_v4_img2, self._p3_panel_etiq_v8_img2,
                       self._p3_panel_etiq_v4_img2_f, self._p3_panel_etiq_v8_img2_f,
                       self._p3_panel_relacional]:
            self._bind_guardar_panel(_panel)

        # Barra de estado
        self._lbl_p3_status = ttk.Label(parent, text="Carga las imágenes para comenzar.  |  Clic derecho sobre cualquier imagen para guardarla.",
                                         font=("Arial", 9), foreground="gray")
        self._lbl_p3_status.pack(pady=3)

    # ---------- Una Imagen (Parte C) ----------

    def _p3_construir_una_imagen(self):
        parent = self._frame_p3_contenido

        # --- Barra de controles ---
        frame_ctrl = ttk.Frame(parent)
        frame_ctrl.pack(fill="x", pady=4, padx=5)

        ttk.Button(frame_ctrl, text="Cargar Imagen", command=self._p3_cargar_img_una).pack(side="left", padx=4)
        ttk.Separator(frame_ctrl, orient='vertical').pack(side="left", fill='y', padx=6)

        ttk.Button(frame_ctrl, text="Convertir a Grises", command=self._p3_grises_una).pack(side="left", padx=4)
        ttk.Separator(frame_ctrl, orient='vertical').pack(side="left", fill='y', padx=6)

        ttk.Label(frame_ctrl, text="Umbral:").pack(side="left")
        self._p3_entry_umbral_una = ttk.Entry(frame_ctrl, width=5)
        self._p3_entry_umbral_una.insert(0, "128")
        self._p3_entry_umbral_una.pack(side="left", padx=2)
        ttk.Button(frame_ctrl, text="Binarizar Fijo", command=self._p3_binarizar_fijo_una).pack(side="left", padx=2)
        ttk.Button(frame_ctrl, text="Binarizar Otsu", command=self._p3_binarizar_otsu_una).pack(side="left", padx=2)
        ttk.Separator(frame_ctrl, orient='vertical').pack(side="left", fill='y', padx=6)

        ttk.Label(frame_ctrl, text="S&P:").pack(side="left")
        self._p3_entry_sp_una = ttk.Entry(frame_ctrl, width=5)
        self._p3_entry_sp_una.insert(0, "0.05")
        self._p3_entry_sp_una.pack(side="left", padx=2)
        ttk.Button(frame_ctrl, text="Aplicar S&P", command=self._p3_ruido_sp_una).pack(side="left", padx=2)
        ttk.Separator(frame_ctrl, orient='vertical').pack(side="left", fill='y', padx=6)

        ttk.Label(frame_ctrl, text="Gauss sigma:").pack(side="left")
        self._p3_entry_gauss_una = ttk.Entry(frame_ctrl, width=5)
        self._p3_entry_gauss_una.insert(0, "25")
        self._p3_entry_gauss_una.pack(side="left", padx=2)
        ttk.Button(frame_ctrl, text="Aplicar Gaussiano", command=self._p3_ruido_gauss_una).pack(side="left", padx=2)
        ttk.Separator(frame_ctrl, orient='vertical').pack(side="left", fill='y', padx=6)

        ttk.Button(frame_ctrl, text="NOT Binaria", command=self._p3_not_una).pack(side="left", padx=4)
        ttk.Separator(frame_ctrl, orient='vertical').pack(side="left", fill='y', padx=6)

        ttk.Button(frame_ctrl, text="Etiquetar V4", command=self._p3_etiquetar_v4_una).pack(side="left", padx=4)
        ttk.Button(frame_ctrl, text="Etiquetar V8", command=self._p3_etiquetar_v8_una).pack(side="left", padx=4)

        # --- Fila superior: procesamiento ---
        frame_proc = ttk.LabelFrame(parent, text="Procesamiento")
        frame_proc.pack(fill="x", padx=5, pady=5)
        for i in range(4):
            frame_proc.columnconfigure(i, weight=1)

        ttk.Label(frame_proc, text="Original",  font=("Arial", 9, "bold")).grid(row=0, column=0, pady=2)
        ttk.Label(frame_proc, text="Grises",    font=("Arial", 9, "bold")).grid(row=0, column=1, pady=2)
        ttk.Label(frame_proc, text="Binaria",   font=("Arial", 9, "bold")).grid(row=0, column=2, pady=2)
        ttk.Label(frame_proc, text="Con Ruido", font=("Arial", 9, "bold")).grid(row=0, column=3, pady=2)

        self._p3_panel_una_orig  = tk.Label(frame_proc, bg="#e0e0e0", relief="sunken", width=22, height=12)
        self._p3_panel_una_orig.grid(row=1, column=0, padx=5, pady=5)
        self._p3_panel_una_gris  = tk.Label(frame_proc, bg="#e0e0e0", relief="sunken", width=22, height=12)
        self._p3_panel_una_gris.grid(row=1, column=1, padx=5, pady=5)
        self._p3_panel_una_bin   = tk.Label(frame_proc, bg="#e0e0e0", relief="sunken", width=22, height=12)
        self._p3_panel_una_bin.grid(row=1, column=2, padx=5, pady=5)
        self._p3_panel_una_ruido = tk.Label(frame_proc, bg="#e0e0e0", relief="sunken", width=22, height=12)
        self._p3_panel_una_ruido.grid(row=1, column=3, padx=5, pady=5)

        # --- Fila inferior: etiquetado ---
        frame_etiq = ttk.LabelFrame(parent, text="Etiquetado")
        frame_etiq.pack(fill="x", padx=5, pady=5)
        for i in range(4):
            frame_etiq.columnconfigure(i, weight=1)

        # Sub-título: con ruido
        ttk.Label(frame_etiq, text="Con Ruido", font=("Arial", 9, "italic"),
                  foreground="#555").grid(row=0, column=0, columnspan=4, pady=(4, 0))

        self._lbl_p3_etiq_v4 = ttk.Label(frame_etiq, text="Etiquetas V4", font=("Arial", 9, "bold"))
        self._lbl_p3_etiq_v4.grid(row=1, column=0, pady=2)
        self._lbl_p3_cont_v4 = ttk.Label(frame_etiq, text="Contornos V4", font=("Arial", 9, "bold"))
        self._lbl_p3_cont_v4.grid(row=1, column=1, pady=2)
        self._lbl_p3_etiq_v8 = ttk.Label(frame_etiq, text="Etiquetas V8", font=("Arial", 9, "bold"))
        self._lbl_p3_etiq_v8.grid(row=1, column=2, pady=2)
        self._lbl_p3_cont_v8 = ttk.Label(frame_etiq, text="Contornos V8", font=("Arial", 9, "bold"))
        self._lbl_p3_cont_v8.grid(row=1, column=3, pady=2)

        self._p3_panel_etiq_v4 = tk.Label(frame_etiq, bg="#e0e0e0", relief="sunken", width=22, height=10)
        self._p3_panel_etiq_v4.grid(row=2, column=0, padx=5, pady=4)
        self._p3_panel_cont_v4 = tk.Label(frame_etiq, bg="#e0e0e0", relief="sunken", width=22, height=10)
        self._p3_panel_cont_v4.grid(row=2, column=1, padx=5, pady=4)
        self._p3_panel_etiq_v8 = tk.Label(frame_etiq, bg="#e0e0e0", relief="sunken", width=22, height=10)
        self._p3_panel_etiq_v8.grid(row=2, column=2, padx=5, pady=4)
        self._p3_panel_cont_v8 = tk.Label(frame_etiq, bg="#e0e0e0", relief="sunken", width=22, height=10)
        self._p3_panel_cont_v8.grid(row=2, column=3, padx=5, pady=4)

        # Sub-título: imagen binaria sin ruido
        ttk.Label(frame_etiq, text="Imagen Binaria (sin ruido)", font=("Arial", 9, "italic"),
                  foreground="#555").grid(row=3, column=0, columnspan=4, pady=(6, 0))

        self._lbl_p3_etiq_v4_f = ttk.Label(frame_etiq, text="Etiquetas V4", font=("Arial", 9, "bold"))
        self._lbl_p3_etiq_v4_f.grid(row=4, column=0, pady=2)
        self._lbl_p3_cont_v4_f = ttk.Label(frame_etiq, text="Contornos V4", font=("Arial", 9, "bold"))
        self._lbl_p3_cont_v4_f.grid(row=4, column=1, pady=2)
        self._lbl_p3_etiq_v8_f = ttk.Label(frame_etiq, text="Etiquetas V8", font=("Arial", 9, "bold"))
        self._lbl_p3_etiq_v8_f.grid(row=4, column=2, pady=2)
        self._lbl_p3_cont_v8_f = ttk.Label(frame_etiq, text="Contornos V8", font=("Arial", 9, "bold"))
        self._lbl_p3_cont_v8_f.grid(row=4, column=3, pady=2)

        self._p3_panel_etiq_v4_f = tk.Label(frame_etiq, bg="#e0e0e0", relief="sunken", width=22, height=10)
        self._p3_panel_etiq_v4_f.grid(row=5, column=0, padx=5, pady=4)
        self._p3_panel_cont_v4_f = tk.Label(frame_etiq, bg="#e0e0e0", relief="sunken", width=22, height=10)
        self._p3_panel_cont_v4_f.grid(row=5, column=1, padx=5, pady=4)
        self._p3_panel_etiq_v8_f = tk.Label(frame_etiq, bg="#e0e0e0", relief="sunken", width=22, height=10)
        self._p3_panel_etiq_v8_f.grid(row=5, column=2, padx=5, pady=4)
        self._p3_panel_cont_v8_f = tk.Label(frame_etiq, bg="#e0e0e0", relief="sunken", width=22, height=10)
        self._p3_panel_cont_v8_f.grid(row=5, column=3, padx=5, pady=4)

        # Clic derecho para guardar en todos los paneles
        for _panel in [self._p3_panel_una_orig, self._p3_panel_una_gris,
                       self._p3_panel_una_bin, self._p3_panel_una_ruido,
                       self._p3_panel_etiq_v4, self._p3_panel_cont_v4,
                       self._p3_panel_etiq_v8, self._p3_panel_cont_v8,
                       self._p3_panel_etiq_v4_f, self._p3_panel_cont_v4_f,
                       self._p3_panel_etiq_v8_f, self._p3_panel_cont_v8_f]:
            self._bind_guardar_panel(_panel)

        # Barra de estado
        self._lbl_p3_status = ttk.Label(parent, text="Carga una imagen para comenzar.  |  Clic derecho sobre cualquier imagen para guardarla.",
                                         font=("Arial", 9), foreground="gray")
        self._lbl_p3_status.pack(pady=3)

    # ---------- Manejadores de eventos P3 — Dos Imágenes ----------

    def _p3_cargar_img1(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.jpeg *.png")])
        if ruta:
            img_bin = self.backend.cargar_img1_p3(ruta)
            self._p2_mostrar(self._p3_panel_img1, img_bin, 200)
            for p in [self._p3_panel_relacional, self._p3_panel_ruido1,
                      self._p3_panel_etiq_v4_img1, self._p3_panel_etiq_v8_img1,
                      self._p3_panel_etiq_v4_img1_f, self._p3_panel_etiq_v8_img1_f]:
                p.config(image='')
            self._lbl_dos_r1_v4.config(text="Etiq. V4\n(ruido)")
            self._lbl_dos_r1_v8.config(text="Etiq. V8\n(ruido)")
            self._lbl_dos_b1_v4.config(text="Etiq. V4\n(binaria)")
            self._lbl_dos_b1_v8.config(text="Etiq. V8\n(binaria)")
            self._lbl_p3_status.config(text="Imagen 1 cargada y binarizada.", foreground="blue")

    def _p3_cargar_img2(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.jpeg *.png")])
        if ruta:
            img_bin = self.backend.cargar_img2_p3(ruta)
            self._p2_mostrar(self._p3_panel_img2, img_bin, 200)
            for p in [self._p3_panel_ruido2,
                      self._p3_panel_etiq_v4_img2, self._p3_panel_etiq_v8_img2,
                      self._p3_panel_etiq_v4_img2_f, self._p3_panel_etiq_v8_img2_f]:
                p.config(image='')
            self._lbl_dos_r2_v4.config(text="Etiq. V4\n(ruido)")
            self._lbl_dos_r2_v8.config(text="Etiq. V8\n(ruido)")
            self._lbl_dos_b2_v4.config(text="Etiq. V4\n(binaria)")
            self._lbl_dos_b2_v8.config(text="Etiq. V8\n(binaria)")
            self._lbl_p3_status.config(text="Imagen 2 cargada y binarizada.", foreground="blue")

    def _p3_op_logica(self):
        operacion = self._p3_combo_logica.get()
        resultado = self.backend.operacion_logica_p3(operacion)
        if resultado is None:
            self._lbl_p3_status.config(
                text="Carga las imágenes necesarias para esta operación.", foreground="red")
            return
        self._p2_mostrar(self._p3_panel_logica, resultado, 200)
        self._lbl_p3_status.config(text=f"Operación lógica {operacion} aplicada.", foreground="green")

    def _p3_op_relacional(self):
        op     = self._p3_combo_relacional.get()
        target = 1 if self._p3_combo_rel_target.get() == "Imagen 1" else 2
        try:
            umbral = max(0, min(255, int(self._p3_entry_umbral_rel.get())))
        except ValueError:
            umbral = 128
        resultado = self.backend.operacion_relacional_p3(op, umbral, target)
        if resultado is None:
            self._lbl_p3_status.config(
                text=f"Primero carga la Imagen {target}.", foreground="red")
            return
        self._p2_mostrar(self._p3_panel_relacional, resultado, 200)
        self._lbl_p3_status.config(
            text=f"Operación relacional (Img{target}) pixel {op} {umbral} aplicada.", foreground="green")

    def _p3_ruido_sp_dos(self):
        try:
            cantidad = float(self._p3_entry_sp_dos.get())
        except ValueError:
            cantidad = 0.05
        resultado = self.backend.ruido_sp_img1_p3(cantidad)
        if resultado is None:
            self._lbl_p3_status.config(text="Primero carga la Imagen 1.", foreground="red")
            return
        self._p2_mostrar(self._p3_panel_ruido1, resultado, 150)
        self._lbl_p3_status.config(text=f"Ruido S&P (cant={cantidad}) aplicado a Imagen 1.", foreground="green")

    def _p3_ruido_gauss_dos(self):
        try:
            sigma = float(self._p3_entry_gauss_dos.get())
        except ValueError:
            sigma = 25.0
        resultado = self.backend.ruido_gauss_img1_p3(sigma)
        if resultado is None:
            self._lbl_p3_status.config(text="Primero carga la Imagen 1.", foreground="red")
            return
        self._p2_mostrar(self._p3_panel_ruido1, resultado, 150)
        self._lbl_p3_status.config(text=f"Ruido Gaussiano (σ={sigma}) aplicado a Imagen 1.", foreground="green")

    def _p3_ruido_sp_img2(self):
        try:
            cantidad = float(self._p3_entry_sp_dos.get())
        except ValueError:
            cantidad = 0.05
        resultado = self.backend.ruido_sp_img2_p3(cantidad)
        if resultado is None:
            self._lbl_p3_status.config(text="Primero carga la Imagen 2.", foreground="red")
            return
        self._p2_mostrar(self._p3_panel_ruido2, resultado, 150)
        self._lbl_p3_status.config(text=f"Ruido S&P (cant={cantidad}) aplicado a Imagen 2.", foreground="green")

    def _p3_ruido_gauss_img2(self):
        try:
            sigma = float(self._p3_entry_gauss_dos.get())
        except ValueError:
            sigma = 25.0
        resultado = self.backend.ruido_gauss_img2_p3(sigma)
        if resultado is None:
            self._lbl_p3_status.config(text="Primero carga la Imagen 2.", foreground="red")
            return
        self._p2_mostrar(self._p3_panel_ruido2, resultado, 150)
        self._lbl_p3_status.config(text=f"Ruido Gaussiano (σ={sigma}) aplicado a Imagen 2.", foreground="green")

    def _p3_etiquetar_dos_img1(self):
        src_ruido = self.backend.img1_ruidosa_p3
        src_bin   = self.backend.img1_bin_p3
        if src_ruido is None:
            self._lbl_p3_status.config(text="Primero aplica ruido a la Imagen 1.", foreground="red")
            return
        c4,  _, cnt4  = self.backend.etiquetar_p3(src_ruido, 4)
        c8,  _, cnt8  = self.backend.etiquetar_p3(src_ruido, 8)
        c4b, _, cnt4b = self.backend.etiquetar_p3(src_bin,   4)
        c8b, _, cnt8b = self.backend.etiquetar_p3(src_bin,   8)
        self._p2_mostrar(self._p3_panel_etiq_v4_img1,   c4,  160)
        self._p2_mostrar(self._p3_panel_etiq_v8_img1,   c8,  160)
        self._p2_mostrar(self._p3_panel_etiq_v4_img1_f, c4b, 160)
        self._p2_mostrar(self._p3_panel_etiq_v8_img1_f, c8b, 160)
        self._lbl_dos_r1_v4.config(text=f"Etiq. V4\n({cnt4} obj ruido)")
        self._lbl_dos_r1_v8.config(text=f"Etiq. V8\n({cnt8} obj ruido)")
        self._lbl_dos_b1_v4.config(text=f"Etiq. V4\n({cnt4b} obj bin)")
        self._lbl_dos_b1_v8.config(text=f"Etiq. V8\n({cnt8b} obj bin)")
        self._lbl_p3_status.config(
            text=f"Img1 — V4: ruido={cnt4} / binaria={cnt4b}  |  V8: ruido={cnt8} / binaria={cnt8b}",
            foreground="green")

    def _p3_etiquetar_dos_img2(self):
        src_ruido = self.backend.img2_ruidosa_p3
        src_bin   = self.backend.img2_bin_p3
        if src_ruido is None:
            self._lbl_p3_status.config(text="Primero aplica ruido a la Imagen 2.", foreground="red")
            return
        c4,  _, cnt4  = self.backend.etiquetar_p3(src_ruido, 4)
        c8,  _, cnt8  = self.backend.etiquetar_p3(src_ruido, 8)
        c4b, _, cnt4b = self.backend.etiquetar_p3(src_bin,   4)
        c8b, _, cnt8b = self.backend.etiquetar_p3(src_bin,   8)
        self._p2_mostrar(self._p3_panel_etiq_v4_img2,   c4,  160)
        self._p2_mostrar(self._p3_panel_etiq_v8_img2,   c8,  160)
        self._p2_mostrar(self._p3_panel_etiq_v4_img2_f, c4b, 160)
        self._p2_mostrar(self._p3_panel_etiq_v8_img2_f, c8b, 160)
        self._lbl_dos_r2_v4.config(text=f"Etiq. V4\n({cnt4} obj ruido)")
        self._lbl_dos_r2_v8.config(text=f"Etiq. V8\n({cnt8} obj ruido)")
        self._lbl_dos_b2_v4.config(text=f"Etiq. V4\n({cnt4b} obj bin)")
        self._lbl_dos_b2_v8.config(text=f"Etiq. V8\n({cnt8b} obj bin)")
        self._lbl_p3_status.config(
            text=f"Img2 — V4: ruido={cnt4} / binaria={cnt4b}  |  V8: ruido={cnt8} / binaria={cnt8b}",
            foreground="green")

    # ---------- Manejadores de eventos P3 — Una Imagen ----------

    def _p3_not_una(self):
        img = self.backend.not_una_p3()
        if img is None:
            self._lbl_p3_status.config(text="Primero binariza la imagen.", foreground="red")
            return
        self._p2_mostrar(self._p3_panel_una_bin, img, 180)
        self._p3_panel_una_ruido.config(image='')   # ruido anterior ya no es válido
        self._lbl_p3_status.config(text="NOT aplicado a la imagen binaria.", foreground="green")

    def _p3_cargar_img_una(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.jpeg *.png")])
        if ruta:
            img = self.backend.cargar_img_una_p3(ruta)
            self._p2_mostrar(self._p3_panel_una_orig, img, 180)
            for panel in [self._p3_panel_una_gris, self._p3_panel_una_bin, self._p3_panel_una_ruido,
                          self._p3_panel_etiq_v4, self._p3_panel_cont_v4,
                          self._p3_panel_etiq_v8, self._p3_panel_cont_v8,
                          self._p3_panel_etiq_v4_f, self._p3_panel_cont_v4_f,
                          self._p3_panel_etiq_v8_f, self._p3_panel_cont_v8_f]:
                panel.config(image='')
            self._lbl_p3_etiq_v4.config(text="Etiquetas V4")
            self._lbl_p3_cont_v4.config(text="Contornos V4")
            self._lbl_p3_etiq_v8.config(text="Etiquetas V8")
            self._lbl_p3_cont_v8.config(text="Contornos V8")
            self._lbl_p3_etiq_v4_f.config(text="Etiquetas V4")
            self._lbl_p3_cont_v4_f.config(text="Contornos V4")
            self._lbl_p3_etiq_v8_f.config(text="Etiquetas V8")
            self._lbl_p3_cont_v8_f.config(text="Contornos V8")
            self._lbl_p3_status.config(text="Imagen cargada.", foreground="blue")

    def _p3_grises_una(self):
        img = self.backend.convertir_gris_una_p3()
        if img is None:
            self._lbl_p3_status.config(text="Primero carga una imagen.", foreground="red")
            return
        self._p2_mostrar(self._p3_panel_una_gris, img, 180)
        self._lbl_p3_status.config(text="Imagen convertida a escala de grises.", foreground="green")

    def _p3_binarizar_fijo_una(self):
        try:
            umbral = max(0, min(255, int(self._p3_entry_umbral_una.get())))
        except ValueError:
            umbral = 128
        img, thresh = self.backend.binarizar_una_p3(umbral)
        if img is None:
            self._lbl_p3_status.config(text="Primero convierte la imagen a grises.", foreground="red")
            return
        self._p2_mostrar(self._p3_panel_una_bin, img, 180)
        self._lbl_p3_status.config(
            text=f"Binarización fija aplicada — umbral = {int(thresh)}.", foreground="green")

    def _p3_binarizar_otsu_una(self):
        img, thresh = self.backend.binarizar_una_p3(None)
        if img is None:
            self._lbl_p3_status.config(text="Primero convierte la imagen a grises.", foreground="red")
            return
        self._p2_mostrar(self._p3_panel_una_bin, img, 180)
        self._lbl_p3_status.config(
            text=f"Binarización Otsu — umbral automático = {int(thresh)}.", foreground="green")

    def _p3_ruido_sp_una(self):
        try:
            cantidad = float(self._p3_entry_sp_una.get())
        except ValueError:
            cantidad = 0.05
        img = self.backend.ruido_sp_una_p3(cantidad)
        if img is None:
            self._lbl_p3_status.config(text="Primero binariza la imagen.", foreground="red")
            return
        self._p2_mostrar(self._p3_panel_una_ruido, img, 180)
        self._lbl_p3_status.config(text=f"Ruido S&P (cant={cantidad}) aplicado.", foreground="green")

    def _p3_ruido_gauss_una(self):
        try:
            sigma = float(self._p3_entry_gauss_una.get())
        except ValueError:
            sigma = 25.0
        img = self.backend.ruido_gauss_una_p3(sigma)
        if img is None:
            self._lbl_p3_status.config(text="Primero convierte la imagen a grises.", foreground="red")
            return
        self._p2_mostrar(self._p3_panel_una_ruido, img, 180)
        self._lbl_p3_status.config(text=f"Ruido Gaussiano (sigma={sigma}) aplicado.", foreground="green")

    def _p3_etiquetar_v4_una(self):
        src = self.backend.img_una_ruidosa_p3 if self.backend.img_una_ruidosa_p3 is not None \
              else self.backend.img_una_bin_p3
        colored, contoured, count = self.backend.etiquetar_p3(src, connectivity=4)
        if colored is None:
            self._lbl_p3_status.config(
                text="Primero binariza la imagen (o aplica ruido).", foreground="red")
            return
        self._p2_mostrar(self._p3_panel_etiq_v4, colored, 180)
        self._p2_mostrar(self._p3_panel_cont_v4, contoured, 180)
        self._lbl_p3_etiq_v4.config(text=f"Etiquetas V4 ({count} obj)")
        self._lbl_p3_cont_v4.config(text=f"Contornos V4 ({count} obj)")

        colored_f, contoured_f, count_f = self.backend.etiquetar_p3(self.backend.img_una_bin_p3, connectivity=4)
        if colored_f is not None:
            self._p2_mostrar(self._p3_panel_etiq_v4_f, colored_f, 180)
            self._p2_mostrar(self._p3_panel_cont_v4_f, contoured_f, 180)
            self._lbl_p3_etiq_v4_f.config(text=f"Etiquetas V4 ({count_f} obj)")
            self._lbl_p3_cont_v4_f.config(text=f"Contornos V4 ({count_f} obj)")

        self._lbl_p3_status.config(
            text=f"Etiquetado V4 — con ruido: {count} obj  |  binaria: {count_f} obj.", foreground="green")

    def _p3_etiquetar_v8_una(self):
        src = self.backend.img_una_ruidosa_p3 if self.backend.img_una_ruidosa_p3 is not None \
              else self.backend.img_una_bin_p3
        colored, contoured, count = self.backend.etiquetar_p3(src, connectivity=8)
        if colored is None:
            self._lbl_p3_status.config(
                text="Primero binariza la imagen (o aplica ruido).", foreground="red")
            return
        self._p2_mostrar(self._p3_panel_etiq_v8, colored, 180)
        self._p2_mostrar(self._p3_panel_cont_v8, contoured, 180)
        self._lbl_p3_etiq_v8.config(text=f"Etiquetas V8 ({count} obj)")
        self._lbl_p3_cont_v8.config(text=f"Contornos V8 ({count} obj)")

        colored_f, contoured_f, count_f = self.backend.etiquetar_p3(self.backend.img_una_bin_p3, connectivity=8)
        if colored_f is not None:
            self._p2_mostrar(self._p3_panel_etiq_v8_f, colored_f, 180)
            self._p2_mostrar(self._p3_panel_cont_v8_f, contoured_f, 180)
            self._lbl_p3_etiq_v8_f.config(text=f"Etiquetas V8 ({count_f} obj)")
            self._lbl_p3_cont_v8_f.config(text=f"Contornos V8 ({count_f} obj)")

        self._lbl_p3_status.config(
            text=f"Etiquetado V8 — con ruido: {count} obj  |  binaria: {count_f} obj.", foreground="green")

    # ==================== PRÁCTICA 4 ====================

    def cargar_interfaz_practica4(self):
        # --- Controles superiores ---
        frame_ctrl = ttk.Frame(self.workspace)
        frame_ctrl.pack(fill="x", pady=8, padx=5)

        ttk.Button(frame_ctrl, text="Subir Imagen", command=self._p4_cargar).pack(side="left", padx=4)
        ttk.Separator(frame_ctrl, orient='vertical').pack(side="left", fill='y', padx=8)

        ttk.Label(frame_ctrl, text="Operación:").pack(side="left")
        self._p4_combo_op = ttk.Combobox(
            frame_ctrl,
            values=["Erosión", "Dilatación", "Apertura", "Cierre"],
            state="readonly", width=12
        )
        self._p4_combo_op.set("Erosión")
        self._p4_combo_op.pack(side="left", padx=4)

        ttk.Label(frame_ctrl, text="Kernel (px):").pack(side="left")
        self._p4_entry_kernel = ttk.Entry(frame_ctrl, width=4)
        self._p4_entry_kernel.insert(0, "5")
        self._p4_entry_kernel.pack(side="left", padx=4)

        ttk.Label(frame_ctrl, text="Iteraciones:").pack(side="left")
        self._p4_entry_iter = ttk.Entry(frame_ctrl, width=4)
        self._p4_entry_iter.insert(0, "1")
        self._p4_entry_iter.pack(side="left", padx=4)

        ttk.Button(frame_ctrl, text="Aplicar", command=self._p4_aplicar).pack(side="left", padx=6)
        ttk.Separator(frame_ctrl, orient='vertical').pack(side="left", fill='y', padx=8)

        ttk.Label(frame_ctrl, text="Umbral:").pack(side="left")
        self._p4_entry_umbral = ttk.Entry(frame_ctrl, width=4)
        self._p4_entry_umbral.insert(0, "128")
        self._p4_entry_umbral.pack(side="left", padx=4)
        ttk.Button(frame_ctrl, text="Binarizar Fijo",
                   command=self._p4_binarizar_fijo).pack(side="left", padx=2)
        ttk.Button(frame_ctrl, text="Binarizar Otsu",
                   command=self._p4_binarizar_otsu).pack(side="left", padx=2)
        ttk.Button(frame_ctrl, text="Restaurar Grises",
                   command=self._p4_restaurar_gris).pack(side="left", padx=4)
        ttk.Separator(frame_ctrl, orient='vertical').pack(side="left", fill='y', padx=8)

        self._p4_ver_matriz_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            frame_ctrl, text="Ver Matrices",
            variable=self._p4_ver_matriz_var,
            command=self._p4_toggle_matrices
        ).pack(side="left", padx=4)

        # --- Marco principal con dos columnas ---
        frame_imgs = ttk.Frame(self.workspace)
        frame_imgs.pack(fill="both", expand=True, pady=5, padx=10)
        frame_imgs.columnconfigure(0, weight=1)
        frame_imgs.columnconfigure(1, weight=1)

        # ---- Panel Izquierdo: Original ----
        self._lf_orig_p4 = ttk.LabelFrame(frame_imgs, text="Imagen Original (Grises)")
        lf_orig = self._lf_orig_p4
        lf_orig.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        self._p4_container_orig = ttk.Frame(lf_orig)
        self._p4_container_orig.pack(padx=5, pady=5)

        self._p4_panel_orig = tk.Label(self._p4_container_orig, bg="#e0e0e0",
                                        relief="sunken", width=40, height=20)
        self._p4_panel_orig.pack()

        self._p4_text_frame_orig = ttk.Frame(self._p4_container_orig)
        self._p4_text_orig = tk.Text(self._p4_text_frame_orig, width=48, height=20,
                                      font=("Courier", 7), state="disabled", wrap="none")
        sb_y_o = ttk.Scrollbar(self._p4_text_frame_orig, orient="vertical",
                                command=self._p4_text_orig.yview)
        sb_x_o = ttk.Scrollbar(self._p4_text_frame_orig, orient="horizontal",
                                command=self._p4_text_orig.xview)
        self._p4_text_orig.configure(yscrollcommand=sb_y_o.set, xscrollcommand=sb_x_o.set)
        sb_y_o.pack(side="right", fill="y")
        sb_x_o.pack(side="bottom", fill="x")
        self._p4_text_orig.pack(side="left", fill="both", expand=True)

        ttk.Button(lf_orig, text="Guardar Original",
                   command=self._p4_guardar_orig).pack(pady=4)

        # ---- Panel Derecho: Resultado ----
        lf_res = ttk.LabelFrame(frame_imgs, text="Imagen Resultante")
        lf_res.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        self._p4_container_res = ttk.Frame(lf_res)
        self._p4_container_res.pack(padx=5, pady=5)

        self._p4_panel_res = tk.Label(self._p4_container_res, bg="#e0e0e0",
                                       relief="sunken", width=40, height=20)
        self._p4_panel_res.pack()

        self._p4_text_frame_res = ttk.Frame(self._p4_container_res)
        self._p4_text_res = tk.Text(self._p4_text_frame_res, width=48, height=20,
                                     font=("Courier", 7), state="disabled", wrap="none")
        sb_y_r = ttk.Scrollbar(self._p4_text_frame_res, orient="vertical",
                                command=self._p4_text_res.yview)
        sb_x_r = ttk.Scrollbar(self._p4_text_frame_res, orient="horizontal",
                                command=self._p4_text_res.xview)
        self._p4_text_res.configure(yscrollcommand=sb_y_r.set, xscrollcommand=sb_x_r.set)
        sb_y_r.pack(side="right", fill="y")
        sb_x_r.pack(side="bottom", fill="x")
        self._p4_text_res.pack(side="left", fill="both", expand=True)

        ttk.Button(lf_res, text="Guardar Resultado",
                   command=self._p4_guardar_res).pack(pady=4)

        # --- Barra de estado ---
        self._lbl_p4_status = ttk.Label(
            self.workspace,
            text="Carga una imagen para comenzar.",
            font=("Arial", 9), foreground="gray"
        )
        self._lbl_p4_status.pack(pady=3)

    def _p4_mostrar(self, panel, img_gris, size=350):
        if img_gris is None:
            return
        self._panel_imgs[id(panel)] = img_gris
        img = cv2.resize(img_gris, (size, size))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)
        panel.config(image=img_tk, width=size, height=size)
        panel.image = img_tk

    def _p4_set_text(self, text_widget, img_gris):
        text_widget.config(state="normal")
        text_widget.delete("1.0", "end")
        if img_gris is None:
            text_widget.insert("end", "(sin imagen)")
        else:
            h, w = img_gris.shape
            MAX = 250
            sub = img_gris[:MAX, :MAX]
            rows, cols = sub.shape
            cw = 3  # ancho de celda (valores 0-255)

            header = f"Shape: {h} × {w} píxeles\n"
            if h > MAX or w > MAX:
                header += f"(Mostrando primeras {rows} filas × {cols} columnas)\n"
            header += "\n"

            top    = "┌" + ("─" * (cw + 2) + "┬") * (cols - 1) + "─" * (cw + 2) + "┐\n"
            mid    = "├" + ("─" * (cw + 2) + "┼") * (cols - 1) + "─" * (cw + 2) + "┤\n"
            bottom = "└" + ("─" * (cw + 2) + "┴") * (cols - 1) + "─" * (cw + 2) + "┘"

            lines = [header, top]
            for i, row in enumerate(sub):
                lines.append("│" + "│".join(f" {int(v):>{cw}} " for v in row) + "│\n")
                if i < rows - 1:
                    lines.append(mid)
            lines.append(bottom)

            text_widget.insert("end", "".join(lines))
        text_widget.config(state="disabled")

    def _p4_cargar(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.jpeg *.png")])
        if not ruta:
            return
        img = self.backend.cargar_imagen_p4(ruta)
        if img is None:
            self._lbl_p4_status.config(text="Error al cargar la imagen.", foreground="red")
            return
        self._p4_mostrar(self._p4_panel_orig, img)
        self._p4_panel_res.config(image='')
        self._p4_set_text(self._p4_text_orig, img)
        self._p4_set_text(self._p4_text_res, None)
        self._lbl_p4_status.config(
            text="Imagen cargada en escala de grises. Selecciona una operación y pulsa Aplicar.",
            foreground="blue")

    def _p4_aplicar(self):
        operacion = self._p4_combo_op.get()
        try:
            kernel_size = max(1, int(self._p4_entry_kernel.get()))
        except ValueError:
            kernel_size = 5
        try:
            iteraciones = max(1, int(self._p4_entry_iter.get()))
        except ValueError:
            iteraciones = 1
        resultado = self.backend.morfologia_p4(operacion, kernel_size, iteraciones)
        if resultado is None:
            self._lbl_p4_status.config(text="Primero carga una imagen.", foreground="red")
            return
        self._p4_mostrar(self._p4_panel_res, resultado)
        self._p4_set_text(self._p4_text_res, resultado)
        self._lbl_p4_status.config(
            text=f"{operacion} aplicada — kernel={kernel_size}×{kernel_size}, iteraciones={iteraciones}.",
            foreground="green")

    def _p4_toggle_matrices(self):
        if self._p4_ver_matriz_var.get():
            self._p4_panel_orig.pack_forget()
            self._p4_panel_res.pack_forget()
            self._p4_text_frame_orig.pack(fill="both", expand=True)
            self._p4_text_frame_res.pack(fill="both", expand=True)
        else:
            self._p4_text_frame_orig.pack_forget()
            self._p4_text_frame_res.pack_forget()
            self._p4_panel_orig.pack()
            self._p4_panel_res.pack()

    def _p4_guardar_orig(self):
        if self.backend.imagen_p4_gris is None:
            return
        ruta = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("Todos", "*.*")]
        )
        if ruta:
            cv2.imwrite(ruta, self.backend.imagen_p4_gris)

    def _p4_guardar_res(self):
        if self.backend.imagen_p4_resultado is None:
            return
        ruta = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("Todos", "*.*")]
        )
        if ruta:
            cv2.imwrite(ruta, self.backend.imagen_p4_resultado)

    def _p4_binarizar_fijo(self):
        try:
            umbral = max(0, min(255, int(self._p4_entry_umbral.get())))
        except ValueError:
            umbral = 128
        img, thresh = self.backend.binarizar_p4(umbral)
        if img is None:
            self._lbl_p4_status.config(text="Primero carga una imagen.", foreground="red")
            return
        self._p4_mostrar(self._p4_panel_orig, img)
        self._p4_set_text(self._p4_text_orig, img)
        self._lf_orig_p4.config(text=f"Imagen Binarizada (umbral fijo={int(thresh)})")
        self._p4_panel_res.config(image='')
        self._p4_set_text(self._p4_text_res, None)
        self._lbl_p4_status.config(
            text=f"Binarización fija — umbral={int(thresh)}. Las operaciones se aplican a esta imagen.",
            foreground="green")

    def _p4_binarizar_otsu(self):
        img, thresh = self.backend.binarizar_p4(None)
        if img is None:
            self._lbl_p4_status.config(text="Primero carga una imagen.", foreground="red")
            return
        self._p4_mostrar(self._p4_panel_orig, img)
        self._p4_set_text(self._p4_text_orig, img)
        self._lf_orig_p4.config(text=f"Imagen Binarizada — Otsu (umbral={int(thresh)})")
        self._p4_panel_res.config(image='')
        self._p4_set_text(self._p4_text_res, None)
        self._lbl_p4_status.config(
            text=f"Binarización Otsu — umbral automático={int(thresh)}. Las operaciones se aplican a esta imagen.",
            foreground="green")

    def _p4_restaurar_gris(self):
        if self.backend.imagen_p4_gris is None:
            return
        self.backend.imagen_p4_bin = None
        self.backend.imagen_p4_trabajo = self.backend.imagen_p4_gris
        self.backend.imagen_p4_resultado = None
        self._p4_mostrar(self._p4_panel_orig, self.backend.imagen_p4_gris)
        self._p4_set_text(self._p4_text_orig, self.backend.imagen_p4_gris)
        self._p4_panel_res.config(image='')
        self._p4_set_text(self._p4_text_res, None)
        self._lf_orig_p4.config(text="Imagen Original (Grises)")
        self._lbl_p4_status.config(text="Restaurada imagen en escala de grises.", foreground="blue")
