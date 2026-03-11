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
        
        # Menú desplegable principal
        self.combo_practicas = ttk.Combobox(self.frame_top, state="readonly", width=30)
        self.combo_practicas['values'] = ("1. Mapas de Calor", "2. Práctica 2 (Próximamente)", "3. Práctica 3 (Próximamente)")
        self.combo_practicas.set("1. Mapas de Calor")
        self.combo_practicas.pack(side="left", padx=10)
        self.combo_practicas.bind("<<ComboboxSelected>>", self.cambiar_practica)

        ttk.Separator(self.root, orient='horizontal').pack(fill='x', pady=5)

        self.workspace = ttk.Frame(self.root, padding="10")
        self.workspace.pack(fill="both", expand=True)

        # Cargar la primera práctica por defecto al iniciar
        self.cargar_interfaz_mapas()

    def cambiar_practica(self, event=None):
        seleccion = self.combo_practicas.get()
        
        # Limpiar el área de trabajo
        for widget in self.workspace.winfo_children():
            widget.destroy()

        # Cargar la interfaz correspondiente
        if "Mapas de Calor" in seleccion:
            self.cargar_interfaz_mapas()
        else:
            ttk.Label(self.workspace, text=f"La {seleccion} aún no está implementada.", font=("Arial", 14)).pack(pady=100)

    def cargar_interfaz_mapas(self):
        # --- Controles de la Práctica 1 ---
        frame_controles = ttk.Frame(self.workspace)
        frame_controles.pack(fill="x", pady=10)

        btn_cargar = ttk.Button(frame_controles, text="Subir Imagen", command=self.evento_cargar_imagen)
        btn_cargar.grid(row=0, column=0, padx=20)

        ttk.Label(frame_controles, text="Mapa de Color:").grid(row=0, column=1, padx=5)
        self.combo_mapas = ttk.Combobox(frame_controles, values=self.backend.obtener_nombres_mapas(), state="readonly")
        self.combo_mapas.set("Grises")
        self.combo_mapas.grid(row=0, column=2, padx=5)

        btn_aplicar = ttk.Button(frame_controles, text="Aplicar mapa", command=self.evento_aplicar_mapa)
        btn_aplicar.grid(row=0, column=3, padx=20)

        # --- Paneles de Imágenes ---
        frame_imagenes = ttk.Frame(self.workspace)
        frame_imagenes.pack(fill="both", expand=True, pady=10)
        
        # Centrar columnas
        for i in range(3):
            frame_imagenes.columnconfigure(i, weight=1)

        # Títulos
        ttk.Label(frame_imagenes, text="Original", font=("Arial", 10, "bold")).grid(row=0, column=0)
        ttk.Label(frame_imagenes, text="Mapa Anterior", font=("Arial", 10, "bold")).grid(row=0, column=1)
        ttk.Label(frame_imagenes, text="Mapa Nuevo", font=("Arial", 10, "bold")).grid(row=0, column=2)

        # Usamos tk.Label con fondo blanco y borde hundido para que se vea el espacio de la imagen
        self.panel_original = tk.Label(frame_imagenes, bg="#e0e0e0", relief="sunken", width=42, height=20)
        self.panel_original.grid(row=1, column=0, padx=10, pady=10)

        self.panel_anterior = tk.Label(frame_imagenes, bg="#e0e0e0", relief="sunken", width=42, height=20)
        self.panel_anterior.grid(row=1, column=1, padx=10, pady=10)

        self.panel_nuevo = tk.Label(frame_imagenes, bg="#e0e0e0", relief="sunken", width=42, height=20)
        self.panel_nuevo.grid(row=1, column=2, padx=10, pady=10)

    def mostrar_en_panel(self, panel, img_cv2):
        if img_cv2 is None: return
        img = cv2.resize(img_cv2, (300, 300))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        img_pil = Image.fromarray(img)
        img_tk = ImageTk.PhotoImage(img_pil)
        
        panel.config(image=img_tk, width=300, height=300)
        panel.image = img_tk  # Prevenir que el recolector de basura elimine la imagen

    def evento_cargar_imagen(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.jpeg *.png")])
        if ruta:
            img = self.backend.cargar_imagen(ruta)
            self.mostrar_en_panel(self.panel_original, img)
            # Limpiar los paneles de resultados al subir una nueva imagen
            self.panel_anterior.config(image='')
            self.panel_nuevo.config(image='')

    def evento_aplicar_mapa(self):
        mapa_seleccionado = self.combo_mapas.get()
        exito = self.backend.aplicar_mapa_color(mapa_seleccionado)
        if exito:
            self.mostrar_en_panel(self.panel_anterior, self.backend.imagen_anterior)
            self.mostrar_en_panel(self.panel_nuevo, self.backend.imagen_nueva)