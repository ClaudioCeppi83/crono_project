import tkinter as tk
from tkinter import font
from timer_engine import TimerEngine

class StopwatchApp:
    """Clase principal para la aplicación de cronómetro con GUI."""

    def __init__(self, root):
        """Inicializa la aplicación."""
        self.root = root
        self.root.title("Cronómetro")
        self.root.geometry("400x500")
        self.root.configure(bg="#282c34")

        self.engine = TimerEngine()
        self._configure_styles()
        self._create_widgets()
        self._update_timer()

    def _configure_styles(self):
        """Configura los estilos para los widgets."""
        self.time_font = font.Font(family="Consolas", size=60, weight="bold")
        self.button_font = font.Font(family="Arial", size=12)
        self.laps_font = font.Font(family="Consolas", size=14)

    def _create_widgets(self):
        """Crea y posiciona los widgets en la ventana."""
        # Frame para el tiempo
        time_frame = tk.Frame(self.root, bg="#282c34")
        time_frame.pack(pady=20)
        self.time_label = tk.Label(time_frame, text="00:00:00.000", font=self.time_font, fg="#61afef", bg="#282c34")
        self.time_label.pack()

        # Frame para los botones
        button_frame = tk.Frame(self.root, bg="#282c34")
        button_frame.pack(pady=10)

        self.start_pause_button = tk.Button(button_frame, text="Iniciar", command=self.toggle_start_pause, width=10, font=self.button_font, bg="#98c379", fg="#282c34")
        self.start_pause_button.pack(side=tk.LEFT, padx=10)

        self.lap_button = tk.Button(button_frame, text="Vuelta", command=self.record_lap, width=10, font=self.button_font, bg="#c678dd", fg="#282c34", state=tk.DISABLED)
        self.lap_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(button_frame, text="Reiniciar", command=self.reset, width=10, font=self.button_font, bg="#e06c75", fg="#282c34", state=tk.DISABLED)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        # Frame para las vueltas
        laps_frame = tk.Frame(self.root, bg="#282c34")
        laps_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        self.laps_listbox = tk.Listbox(laps_frame, font=self.laps_font, bg="#3b4048", fg="#abb2bf", selectbackground="#61afef", borderwidth=0, highlightthickness=0)
        self.laps_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def toggle_start_pause(self):
        """Inicia o pausa el cronómetro."""
        if self.engine.is_running:
            self.engine.pause()
            self.start_pause_button.config(text="Reanudar", bg="#98c379")
            self.lap_button.config(state=tk.DISABLED)
        else:
            self.engine.start()
            self.start_pause_button.config(text="Pausar", bg="#e5c07b")
            self.lap_button.config(state=tk.NORMAL)
            self.reset_button.config(state=tk.NORMAL)

    def record_lap(self):
        """Registra una vuelta."""
        self.engine.record_lap()
        self.laps_listbox.delete(0, tk.END)
        for i, lap_time in enumerate(reversed(self.engine.laps)):
            formatted_time = self._format_time(lap_time)
            self.laps_listbox.insert(tk.END, f" Vuelta {len(self.engine.laps) - i}: {formatted_time}")

    def reset(self):
        """Reinicia el cronómetro."""
        self.engine.reset()
        self.time_label.config(text="00:00:00.000")
        self.start_pause_button.config(text="Iniciar", bg="#98c379")
        self.lap_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)
        self.laps_listbox.delete(0, tk.END)

    def _update_timer(self):
        """Actualiza el display del tiempo cada 10ms."""
        current_time = self.engine.get_current_time()
        formatted_time = self._format_time(current_time)
        self.time_label.config(text=formatted_time)
        self.root.after(10, self._update_timer)

    def _format_time(self, seconds):
        """Formatea el tiempo en HH:MM:SS.ms."""
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.{milliseconds:03d}"

if __name__ == "__main__":
    root = tk.Tk()
    app = StopwatchApp(root)
    root.mainloop()