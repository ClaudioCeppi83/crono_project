import time
import os
from timer_engine import TimerEngine

def print_menu():
    """Imprime el menú de opciones en la consola."""
    print("\n--- Cronómetro Secuencial ---")
    print("1. Iniciar / Reanudar")
    print("2. Pausar")
    print("3. Registrar Vuelta (Lap)")
    print("4. Resetear")
    print("5. Salir")
    print("-----------------------------")

def clear_screen():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """Función principal de la aplicación de cronómetro en consola."""
    engine = TimerEngine()

    while True:
        clear_screen()
        print_menu()

        current_time = engine.get_current_time()
        status = "Corriendo" if engine.is_running else "Pausado"

        print(f"\nTiempo Actual: {current_time:.2f}s ({status})")
        if engine.laps:
            print(f"Vueltas: {[f'{lap:.2f}s' for lap in engine.laps]}")

        choice = input("\nElige una opción: ")

        if choice == '1':
            engine.start()
        elif choice == '2':
            engine.pause()
        elif choice == '3':
            engine.record_lap()
        elif choice == '4':
            engine.reset()
        elif choice == '5':
            print("Saliendo del cronómetro.")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")
            time.sleep(1)

if __name__ == "__main__":
    main()