import tkinter as tk
from gui import StopwatchApp

def main():
    """Función principal para iniciar la aplicación de cronómetro con GUI."""
    root = tk.Tk()
    app = StopwatchApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()