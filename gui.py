import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import tkinter as tk
from tkinter import font, simpledialog, messagebox
from timer_engine import TimerEngine
from event_manager import EventManager, EventMode
from storage_service import StorageService
import uuid
from datetime import datetime



class StopwatchApp:
    """Clase principal para la aplicación de cronómetro con GUI rediseñada."""

    def __init__(self, root):
        """Inicializa la aplicación."""
        self.root = root
        self.root.title("ChronoFlow")
        self.root.geometry("400x650")
        self.root.resizable(False, False)

        self.engine = TimerEngine()
        self.event_manager = EventManager()
        self.storage = StorageService()
        self.session_id = str(uuid.uuid4())
        self.session_start = datetime.now().isoformat()
        self.session_name = None

        self._configure_styles_and_colors()
        self._create_ui()
        self._update_timer()

        self.change_mode(EventMode.INFINITE) # Iniciar en modo infinito por defecto

    def _configure_styles_and_colors(self):
        """Configura los estilos y la paleta de colores para los widgets."""
        self.BG_COLOR = "#1A1A1A"
        self.FG_COLOR = "#FFFFFF"
        self.ACCENT_COLOR = "#39FF14"
        self.ACCENT_DARK_COLOR = "#2F4F2F"
        self.CARD_COLOR = "#2C2C2C"
        self.root.configure(bg=self.BG_COLOR)

        self.time_font = font.Font(family="Segoe UI Variable Display", size=50, weight="bold")
        self.time_ms_font = font.Font(family="Segoe UI Variable Display", size=50, weight="normal")
        self.button_font = font.Font(family="Segoe UI Variable", size=16, weight="bold")
        self.laps_header_font = font.Font(family="Segoe UI Variable", size=18, weight="bold")
        self.laps_font = font.Font(family="Segoe UI Variable", size=14)
        self.menu_button_font = font.Font(family="Segoe UI Symbol", size=20)
        self.reset_font = font.Font(family="Segoe UI Variable", size=12, underline=True)
        self.menu_font = font.Font(family="Segoe UI Variable", size=14)

    def _create_ui(self):
        """Crea y posiciona todos los widgets de la interfaz."""
        self._create_top_bar()
        self._create_timer_display()
        self._create_control_buttons()
        self._create_laps_display()
        self._create_side_menu()

        # Bind event to close side menu when clicking outside
        self.root.bind("<Button-1>", self._hide_menu_if_visible)

    def _create_top_bar(self):
        top_bar = tk.Frame(self.root, bg=self.BG_COLOR)
        top_bar.pack(fill='x', pady=10, padx=20)

        self.menu_button = tk.Button(top_bar, text="☰", font=self.menu_button_font, bg=self.BG_COLOR, fg=self.FG_COLOR, command=self.toggle_side_menu, relief='flat', borderwidth=0)
        self.menu_button.pack(side='left')

        self.mode_label = tk.Label(top_bar, text="", font=self.menu_font, fg=self.ACCENT_COLOR, bg=self.BG_COLOR)
        self.mode_label.pack(side='left', expand=True)

        self.settings_button = tk.Button(top_bar, text="⚙", font=self.menu_button_font, bg=self.BG_COLOR, fg=self.FG_COLOR, relief='flat', borderwidth=0)
        self.settings_button.pack(side='right')

    def _create_timer_display(self):
        time_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        time_frame.pack(pady=30)

        self.time_label = tk.Label(time_frame, text="00:00:00", font=self.time_font, fg=self.FG_COLOR, bg=self.BG_COLOR)
        self.time_label.pack(side='left')

        self.time_ms_label = tk.Label(time_frame, text=".00", font=self.time_ms_font, fg=self.ACCENT_COLOR, bg=self.BG_COLOR)
        self.time_ms_label.pack(side='left')

    def _create_control_buttons(self):
        button_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        button_frame.pack(pady=10, fill='x', padx=40)

        self.start_pause_button = tk.Button(button_frame, text="Start", command=self.toggle_start_pause, font=self.button_font, bg=self.ACCENT_COLOR, fg="#000000", relief='flat', borderwidth=0, width=10, height=2)
        self.start_pause_button.pack(side=tk.LEFT, expand=True, padx=5)

        self.lap_button = tk.Button(button_frame, text="Lap", command=self.record_lap, font=self.button_font, bg=self.ACCENT_DARK_COLOR, fg=self.FG_COLOR, relief='flat', borderwidth=0, width=10, height=2, state=tk.DISABLED)
        self.lap_button.pack(side=tk.RIGHT, expand=True, padx=5)

        reset_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        reset_frame.pack(pady=10)
        self.reset_button = tk.Button(reset_frame, text="Reset", command=self.reset, font=self.reset_font, bg=self.BG_COLOR, fg=self.FG_COLOR, relief='flat', borderwidth=0, state=tk.DISABLED, cursor="hand2")
        self.reset_button.pack()

    def _create_laps_display(self):
        laps_header_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        laps_header_frame.pack(fill='x', padx=40, pady=(20, 5))
        tk.Label(laps_header_frame, text="Laps", font=self.laps_header_font, fg=self.FG_COLOR, bg=self.BG_COLOR).pack(side='left')

        laps_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        laps_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=40)

        self.laps_listbox = tk.Listbox(laps_frame, font=self.laps_font, bg=self.CARD_COLOR, fg=self.FG_COLOR, selectbackground=self.ACCENT_COLOR, borderwidth=0, highlightthickness=0, relief='flat')
        self.laps_listbox.pack(fill=tk.BOTH, expand=True)

    def _create_side_menu(self):
        self.side_menu_frame = tk.Frame(self.root, bg=self.CARD_COLOR, width=250, height=self.root.winfo_height())
        # La posición se gestionará con place()

        tk.Label(self.side_menu_frame, text="Timer Mode", font=self.laps_header_font, bg=self.CARD_COLOR, fg=self.ACCENT_COLOR).pack(pady=20, padx=20, anchor='w')
        
        tk.Button(self.side_menu_frame, text="Infinite", font=self.menu_font, bg=self.CARD_COLOR, fg=self.FG_COLOR, relief='flat', command=lambda: self.change_mode(EventMode.INFINITE)).pack(fill='x', padx=20, pady=5)
        tk.Button(self.side_menu_frame, text="Max Laps", font=self.menu_font, bg=self.CARD_COLOR, fg=self.FG_COLOR, relief='flat', command=lambda: self.change_mode(EventMode.MAXIMUM)).pack(fill='x', padx=20, pady=5)
        tk.Button(self.side_menu_frame, text="Predefined Names", font=self.menu_font, bg=self.CARD_COLOR, fg=self.FG_COLOR, relief='flat', command=lambda: self.change_mode(EventMode.PREDEFINED)).pack(fill='x', padx=20, pady=5)

        tk.Frame(self.side_menu_frame, height=1, bg=self.BG_COLOR).pack(fill='x', pady=10, padx=20)

        tk.Button(self.side_menu_frame, text="Session History", font=self.menu_font, bg=self.CARD_COLOR, fg=self.FG_COLOR, relief='flat', command=self.show_history).pack(fill='x', padx=20, pady=5)
        tk.Button(self.side_menu_frame, text="Save Session", font=self.menu_font, bg=self.CARD_COLOR, fg=self.FG_COLOR, relief='flat', command=self.save_session_prompt).pack(fill='x', padx=20, pady=5)

        self.side_menu_visible = False

    def toggle_side_menu(self):
        if self.side_menu_visible:
            self.side_menu_frame.place_forget()
        else:
            self.side_menu_frame.place(x=0, y=0, relheight=1.0)
            self.side_menu_frame.lift() # Ensure menu is on top
        self.side_menu_visible = not self.side_menu_visible

    def _hide_menu_if_visible(self, event):
        """Close the side menu if a click occurs outside of it."""
        if self.side_menu_visible and event.widget != self.menu_button:
            # Check if the click was inside the side menu frame
            is_in_menu = False
            curr = event.widget
            while curr is not None:
                if curr == self.side_menu_frame:
                    is_in_menu = True
                    break
                try:
                    curr = curr.master
                except AttributeError:
                    break
            
            if not is_in_menu:
                self.toggle_side_menu()

    def change_mode(self, mode):
        kwargs = {}
        if mode == EventMode.MAXIMUM:
            max_laps = simpledialog.askinteger("Max Laps", "Enter the maximum number of laps:", minvalue=1, parent=self.root)
            if max_laps is None: return
            kwargs['max_laps'] = max_laps
        elif mode == EventMode.PREDEFINED:
            names = self._ask_predefined_names()
            if not names:
                return
            kwargs['lap_names'] = names

        self.event_manager.configure_session(mode, **kwargs)
        self.reset()
        self.update_mode_display()
        if self.side_menu_visible:
            self.toggle_side_menu()



    def toggle_start_pause(self):
        """Alterna entre iniciar y pausar el cronómetro."""
        if self.engine.is_running:
            self.engine.pause()
            self.start_pause_button.config(text="Start", bg=self.ACCENT_COLOR, fg="#000000")
        else:
            self.engine.start()
            self.start_pause_button.config(text="Pause", bg="#FF4136", fg=self.FG_COLOR)
        self.lap_button.config(state=tk.NORMAL if self.engine.is_running else tk.DISABLED)
        self.reset_button.config(state=tk.NORMAL)

    def record_lap(self):
        """Registra una vuelta y la muestra en la lista."""
        if not self.event_manager.can_record_lap():
            messagebox.showwarning("Límite de vueltas", "Se ha alcanzado el número máximo de vueltas.")
            return

        current_time = self.engine.get_current_time()
        time_str, ms_str = self._format_time(current_time)
        lap_time_str = f"{time_str}.{ms_str}"

        self.event_manager.record_lap(lap_time_str)
        
