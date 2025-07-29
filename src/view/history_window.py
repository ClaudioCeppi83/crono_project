import tkinter as tk
from tkinter import font

class HistoryWindow(tk.Toplevel):
    """Ventana para mostrar el historial de sesiones guardadas."""

    def __init__(self, parent, sessions):
        super().__init__(parent)
        self.title("Historial de Sesiones")
        self.geometry("600x500")
        self.configure(bg="#2C2C2C")

        self._configure_fonts()
        self._create_widgets(sessions)

    def _configure_fonts(self):
        self.header_font = font.Font(family="Segoe UI Variable", size=18, weight="bold")
        self.session_font = font.Font(family="Segoe UI Variable", size=14)

    def _create_widgets(self, sessions):
        main_frame = tk.Frame(self, bg="#2C2C2C")
        main_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_frame, bg="#2C2C2C", highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = tk.Frame(canvas, bg="#2C2C2C")
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        if not sessions:
            tk.Label(scrollable_frame, text="No hay sesiones guardadas.", bg="#2C2C2C", fg="#FFFFFF", font=self.session_font).pack(pady=20)
        else:
            for session in sessions:
                self._create_session_card(scrollable_frame, session)

    def _create_session_card(self, parent, session):
        card = tk.Frame(parent, bg="#1A1A1A", relief="raised", borderwidth=1, padx=10, pady=10)
        card.pack(fill="x", padx=20, pady=10)

        name = session.get("session_name", "Sin nombre")
        start_time_str = session.get("start_time", "").replace("T", " ").split(".")[0]
        mode = session.get("mode", "N/A")
        laps = session.get("laps", [])

        tk.Label(card, text=name, font=self.header_font, fg="#39FF14", bg="#1A1A1A").pack(anchor="w")
        tk.Label(card, text=f"Inicio: {start_time_str} | Modo: {mode}", font=self.session_font, fg="#FFFFFF", bg="#1A1A1A").pack(anchor="w")

        if laps:
            laps_frame = tk.Frame(card, bg="#1A1A1A")
            laps_frame.pack(fill="x", pady=5)
            for i, lap in enumerate(laps):
                lap_info = f"{i+1}. {lap.get('name', '')}: {lap.get('time', '')}"
                tk.Label(laps_frame, text=lap_info, font=self.session_font, fg="#FFFFFF", bg="#1A1A1A").pack(anchor="w")
