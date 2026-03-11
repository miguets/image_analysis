import tkinter as tk
from backend import ProcesadorImagenes
from frontend import InterfazApp

def main():
    backend = ProcesadorImagenes()
    
    root = tk.Tk()
    
    app = InterfazApp(root, backend)
    
    root.mainloop()

if __name__ == "__main__":
    main()