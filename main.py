import tkinter as tk
from src.controller.app_controller import AppController

def main():
    """Función principal para iniciar la aplicación de cronómetro."""
    root = tk.Tk()
    _ = AppController(root)
    root.mainloop()

if __name__ == "__main__":
    main()