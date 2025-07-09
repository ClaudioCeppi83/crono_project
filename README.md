# ChronoFlow v1.1.0

![ChronoFlow](https://raw.githubusercontent.com/ClaudioCeppi83/crono_project/main/assets/screenshot.png)

**ChronoFlow** es una aplicación de cronómetro de alta precisión, moderna y fácil de usar, desarrollada en Python con una interfaz gráfica creada con `tkinter`. Es ideal para medir el tiempo en cualquier tarea que requiera precisión y un registro detallado de vueltas.

---

## ✨ Características

- **Alta Precisión**: Muestra el tiempo con una precisión de milisegundos (`HH:MM:SS.ms`).
- **Interfaz Moderna y Limpia**: Diseño intuitivo y agradable a la vista para una experiencia de usuario fluida.
- **Múltiples Modos de Operación**:
  - **Modo Infinito**: Registra vueltas sin límite.
  - **Modo Máximo de Vueltas**: Detiene el cronómetro automáticamente después de un número predefinido de vueltas.
  - **Modo Nombres Predefinidos**: Asigna nombres personalizados a cada vuelta de una lista predefinida.
- **Controles Intuitivos**: Botones claros para iniciar, pausar, reanudar, registrar vueltas y reiniciar.
- **Registro de Vueltas Detallado**: Guarda y muestra una lista de todas las vueltas registradas en tiempo real.
- **Historial de Sesiones**: Guarda tus sesiones de cronometraje y revísalas más tarde.
- **Ligera y Rápida**: Construida con `tkinter`, no requiere dependencias pesadas.

---

## 🚀 Cómo Empezar

Para ejecutar ChronoFlow en tu sistema, solo necesitas tener Python 3 instalado.

### Prerrequisitos

- [Python 3.6+](https://www.python.org/downloads/)

### Instalación

1. **Clona el repositorio:**
   ```sh
   git clone https://github.com/ClaudioCeppi83/crono_project.git
   ```

2. **Navega al directorio del proyecto:**
   ```sh
   cd crono_project
   ```

---

## 💻 Uso

Para iniciar la aplicación, ejecuta el archivo `gui.py`:

```sh
python gui.py
```

Una vez iniciada, la aplicación comenzará en **Modo Infinito** por defecto. Puedes cambiar el modo de operación desde el menú **Modo** en la parte superior de la ventana. El modo seleccionado se mostrará directamente en la ventana principal, debajo del cronómetro.

---

## 🛠️ Construido Con

- [Python](https://www.python.org/) - El lenguaje de programación principal.
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - Para la interfaz gráfica de usuario.

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2024-05-24

### Added
- **Múltiples Modos de Operación**: Se han añadido los modos 'Infinito', 'Máximo de Vueltas' y 'Nombres Predefinidos' para una mayor flexibilidad en el cronometraje.
- **Menú de Modos**: Se ha implementado un menú en la barra superior para cambiar fácilmente entre los diferentes modos de operación.
- **Visualización del Modo Actual**: El modo de cronometraje seleccionado ahora se muestra directamente en la ventana principal.
- **Historial de Sesiones**: Funcionalidad para guardar y ver sesiones de cronometraje anteriores.
- **Entrada Multilínea**: Se ha mejorado la entrada de nombres predefinidos para aceptar múltiples líneas.

## [1.0.0] - 2024-05-23

### Added
- **Fase 1: Creación del MVP**
  - Funcionalidad básica de cronómetro: iniciar, pausar y reiniciar.
  - Registro de vueltas simple.
  - Interfaz gráfica inicial con Tkinter.
  - Almacenamiento de la sesión en un archivo JSON.

### Changed
- **Flujo de Inicio**: La aplicación ahora se inicia directamente en el modo 'Infinito', eliminando la ventana de configuración inicial.
- **Comportamiento del Botón 'Vuelta'**: 
  - En el modo 'Máximo de Vueltas', el botón 'Vuelta' cambia a 'Stop' cuando se alcanza el número máximo de vueltas.
  - En el modo 'Nombres Predefinidos', el botón 'Vuelta' cambia a 'Stop' después de registrar la última vuelta con nombre.
- **Lógica de Reinicio**: Se ha mejorado la función de reinicio para restaurar completamente el estado de la aplicación, incluyendo el gestor de eventos.

### Fixed
- El botón de inicio/pausa ahora se reactiva correctamente después de un reinicio.
