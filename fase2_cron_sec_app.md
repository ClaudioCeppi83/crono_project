¡Perfecto\! Aquí tienes un plan de desarrollo detallado en formato Markdown para la **Fase 2**.

-----

## Plan de Desarrollo: Fase 2 - Configuración de Eventos

El objetivo de esta fase es implementar la lógica y la interfaz necesarias para que el usuario pueda configurar el tipo de sesión de cronometraje antes de iniciarla.

### 1\. Lógica de Negocio (Backend)

El foco aquí es crear la estructura de datos y la lógica que soportará los diferentes modos de evento, independientemente de la interfaz de usuario.

  * **1.1. Definir los Modos de Evento:**

      * Crear una enumeración (`Enum`) para representar los modos de forma segura y clara.
        ```python
        from enum import Enum, auto

        class EventMode(Enum):
            INFINITE = auto()
            PREDEFINED = auto()
            MAXIMUM = auto()
        ```

  * **1.2. Desarrollar el `EventManager`:**

      * Crear una nueva clase `EventManager`.
      * **Atributos:**
          * `mode`: Almacenará el `EventMode` seleccionado.
          * `lap_names`: Una lista con los nombres personalizados para el modo `PREDEFINED`.
          * `max_laps`: Un entero para el límite en el modo `MAXIMUM`.
          * `next_lap_index`: Un contador para saber qué vuelta es la siguiente.
      * **Métodos:**
          * `configure_session(mode, **kwargs)`: Un método para establecer la configuración.
          * `get_next_lap_name()`: Devuelve el nombre de la siguiente vuelta según el modo.
          * `can_record_lap()`: Devuelve `True` si aún se pueden registrar vueltas.

  * **1.3. Refactorizar el `TimerEngine`:**

      * Modificar la estructura de datos de las vueltas. En lugar de una simple lista de `floats`, la lista `laps` ahora contendrá tuplas o un pequeño objeto de datos: `(nombre_vuelta, tiempo_vuelta)`.
      * Actualizar el método `record_lap()` para que acepte un nombre como parámetro: `record_lap(name: str)`.

-----

### 2\. Interfaz de Usuario (Frontend)

Aquí se construye la parte visual que el usuario utilizará para configurar la sesión.

  * **2.1. Crear la Pantalla de Configuración (`ConfigView`):**

      * Diseñar una nueva ventana o vista que será lo primero que vea el usuario.
      * **Componentes:**
          * Un grupo de botones de radio o un menú desplegable para seleccionar el `EventMode`.
          * Un área que cambia dinámicamente según la selección:
              * **Modo Predefinido:** Un campo de texto para añadir nombres de vueltas a una lista visible.
              * **Modo Máximo:** Un campo de entrada numérica.
              * **Modo Infinito:** Ningún campo adicional es necesario.
          * Un botón de **"Iniciar Sesión"**.

  * **2.2. Actualizar la Pantalla Principal (`MainView`):**

      * Modificar la lista de vueltas para que ahora muestre el **nombre** y el **tiempo** de cada una.
      * La lógica del botón "Vuelta" debe ser actualizada para que su texto pueda cambiar dinámicamente (ej., mostrar el nombre de la siguiente vuelta predefinida).

-----

### 3\. Integración y Lógica de la Aplicación

Este es el paso final donde se une el backend y el frontend para crear el flujo funcional completo.

  * **3.1. Establecer el Flujo de la Aplicación:**

      * La aplicación ahora se inicia en la `ConfigView`.
      * Al pulsar "Iniciar Sesión", se crea una instancia del `EventManager` con la configuración seleccionada.
      * Se abre la `MainView`, pasándole la instancia configurada del `EventManager`.

  * **3.2. Conectar la Lógica a los Botones:**

      * Al pulsar el botón **"Vuelta"** en `MainView`:
        1.  La app consulta al `EventManager` si se puede registrar una vuelta usando `can_record_lap()`.
        2.  Si es así, obtiene el nombre de la vuelta con `get_next_lap_name()`.
        3.  Llama a `timer_engine.record_lap(name=...)` con el nombre obtenido.
        4.  Se actualiza la lista en la UI.
        5.  Si `can_record_lap()` devuelve `False`, el botón "Vuelta" se deshabilita.