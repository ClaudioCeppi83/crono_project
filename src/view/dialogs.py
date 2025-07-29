import tkinter as tk
from tkinter import simpledialog, messagebox

class Dialogs:
    """Clase para manejar los diálogos de la aplicación."""

    @staticmethod
    def ask_max_laps(parent):
        """Pregunta al usuario por el número máximo de vueltas."""
        return simpledialog.askinteger(
            "Max Laps", 
            "Enter the maximum number of laps:", 
            minvalue=1, 
            parent=parent
        )

    @staticmethod
    def ask_predefined_names(parent):
        """Muestra un diálogo para que el usuario ingrese nombres predefinidos."""
        dialog = tk.Toplevel(parent)
        dialog.title("Predefined Names")
        dialog.geometry("300x400")
        dialog.configure(bg="#2C2C2C")

        tk.Label(dialog, text="Enter one name per line:", bg="#2C2C2C", fg="#FFFFFF").pack(pady=10)
        text_widget = tk.Text(dialog, height=15, width=35, bg="#1A1A1A", fg="#FFFFFF", insertbackground="#FFFFFF")
        text_widget.pack(pady=10, padx=10)

        names = []
        def on_ok():
            nonlocal names
            names = [name.strip() for name in text_widget.get("1.0", tk.END).splitlines() if name.strip()]
            dialog.destroy()

        tk.Button(dialog, text="OK", command=on_ok, bg="#39FF14", fg="#000000").pack(pady=10)
        
        parent.wait_window(dialog)
        return names

    @staticmethod
    def ask_session_name(parent):
        """Pregunta al usuario por un nombre para la sesión."""
        return simpledialog.askstring("Save Session", "Enter a name for the session (optional):", parent=parent)

    @staticmethod
    def show_warning(title, message):
        """Muestra un mensaje de advertencia."""
        messagebox.showwarning(title, message)

    @staticmethod
    def show_info(title, message):
        """Muestra un mensaje informativo."""
        messagebox.showinfo(title, message)
