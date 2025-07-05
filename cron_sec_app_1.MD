## Documento de Desarrollo de Proyecto: Cronómetro Secuencial Avanzado

**Versión:** 1.0
**Fecha:** 2024-07-01
**Autor:** Gemini AI (Actuando como Arquitecto de Software)

### 1. Resumen Ejecutivo

Este documento describe los requisitos, la arquitectura y el plan de desarrollo para una aplicación de **cronómetro secuencial avanzado**. El objetivo es crear una herramienta precisa y flexible que permita a los usuarios no solo medir el tiempo total de un evento, sino también registrar múltiples subeventos o "laps" dentro de esa misma sesión. La aplicación ofrecerá modos de configuración personalizables, desde registros ilimitados con nombres genéricos hasta un número predefinido de subeventos con nombres específicos. Todos los registros se guardarán de forma persistente para su posterior consulta.

---

### 2. Objetivos y Alcance

#### **2.1. Objetivos Principales**

* **O-1:** Desarrollar un cronómetro de alta precisión, fiable y con una interfaz de usuario intuitiva.
* **O-2:** Implementar una funcionalidad robusta para registrar tiempos intermedios (subeventos) sin detener el cronómetro principal.
* **O-3:** Ofrecer al usuario un sistema de configuración de eventos flexible para adaptarse a diferentes casos de uso.
* **O-4:** Garantizar la persistencia de los datos, guardando todas las sesiones y sus registros asociados para consulta futura.

#### **2.2. Alcance del Proyecto (En Alcance)**

* Funcionalidad de cronómetro estándar: Iniciar, Pausar, Reanudar, Reiniciar.
* Registro de tiempos intermedios (laps/splits).
* Creación de "Plantillas de Evento" con tres modos:
    1.  **Modo Infinito:** Sin límite de subeventos, nombres genéricos (Ej: "Registro 1", "Registro 2").
    2.  **Modo Predefinido:** Número exacto de subeventos con nombres personalizados por el usuario antes de iniciar (Ej: "Calentamiento", "Serie 1", "Enfriamiento").
    3.  **Modo Máximo:** Un número máximo de subeventos configurables, permitiendo flexibilidad pero con un tope.
* Guardado de cada sesión de cronometraje. Cada sesión incluirá el tiempo total, la fecha/hora de inicio y una lista de todos sus subeventos.
* Cada subevento guardará su nombre, el tiempo exacto en el que fue registrado, la fecha y la hora.
* Una pantalla de "Historial" para ver, buscar y eliminar sesiones guardadas.

#### **2.3. Fuera de Alcance (Para futuras versiones)**

* Sincronización en la nube entre dispositivos.
* Funciones sociales (compartir resultados).
* Exportación de datos a formatos como CSV o PDF.
* Estadísticas avanzadas o gráficos de rendimiento.
* Cuentas de usuario y perfiles.

---

### 3. Arquitectura y Diseño Técnico

#### **3.1. Modelo de Datos**

Se definen dos entidades principales para estructurar la información.

**Entidad 1: `SesionEvento`**
Representa una sesión completa de cronometraje.

| Atributo | Tipo de Dato | Descripción | Ejemplo |
| :--- | :--- | :--- | :--- |
| `id` | UUID / String | Identificador único de la sesión. | "f47ac10b-58cc-4372-a567-0e02b2c3d479" |
| `nombreEvento`| String | Nombre descriptivo de la sesión. | "Entrenamiento de Natación" |
| `fechaInicio` | Timestamp | Fecha y hora exactas del inicio. | "2024-07-01T10:00:00Z" |
| `duracionTotal`| Double | Tiempo total transcurrido en segundos. | 915.75 |
| `modoEvento` | Enum | Tipo de configuración usada. | `PREDEFINIDO` |
| `registros` | Array[`RegistroTiempo`] | Relación Uno-a-Muchos con los subeventos. | `[...]` |

**Entidad 2: `RegistroTiempo`**
Representa un subevento o lap individual dentro de una `SesionEvento`.

| Atributo | Tipo de Dato | Descripción | Ejemplo |
| :--- | :--- | :--- | :--- |
| `id` | UUID / String | Identificador único del registro. | "a1b2c3d4-e5f6-7890-1234-567890abcdef" |
| `nombreRegistro`| String | Nombre del subevento. | "Primeros 50m Crol" |
| `tiempoRegistrado` | Double | Tiempo transcurrido desde el inicio de la sesión en segundos. | 32.50 |
| `fechaHoraRegistro`| Timestamp | Fecha y hora exactas del registro. | "2024-07-01T10:00:32Z" |

#### **3.2. Arquitectura de la Aplicación (MVVM)**

Se sugiere una arquitectura **Model-View-ViewModel (MVVM)** para separar la lógica de negocio de la interfaz de usuario, facilitando el mantenimiento y las pruebas.

* **Model:** Las entidades `SesionEvento` y `RegistroTiempo`. Define la estructura de los datos.
* **View:** La interfaz de usuario (UI). Compuesta por las pantallas (cronómetro, configuración, historial). Es reactiva y se actualiza en función de los cambios en el ViewModel.
* **ViewModel:** Contiene toda la lógica de la aplicación. Gestiona el estado del cronómetro (`isRunning`, `elapsedTime`), maneja la configuración de eventos, procesa las acciones del usuario (iniciar, registrar lap) y se comunica con los servicios de persistencia.

#### **3.3. Componentes Clave**

1.  **`TimerEngine` (Motor del Cronómetro):**
    * Una clase o servicio central responsable de la lógica del tiempo.
    * Utilizará un temporizador de alta resolución del sistema (`CADisplayLink` en iOS, `Choreographer` en Android) para garantizar la precisión, actualizando el tiempo transcurrido en cada frame.
    * Expondrá métodos como `start()`, `pause()`, `reset()`, `recordLap()`.
    * Mantendrá el estado actual: `tiempoTranscurrido`, `estaCorriendo`, `laps[]`.

2.  **`StorageService` (Servicio de Persistencia):**
    * Abstrae la lógica de guardado y carga de datos.
    * Implementará métodos como `guardarSesion(SesionEvento)`, `obtenerSesiones()`, `eliminarSesion(id)`.
    * Podría usar una base de datos local como **SQLite**, **Realm** o simplemente guardar los datos en archivos **JSON** en el almacenamiento del dispositivo.

3.  **`EventManager` (Gestor de Eventos):**
    * Lógica para gestionar la configuración de los modos de evento.
    * Responsable de preparar la sesión de cronometraje según la configuración seleccionada por el usuario (nombres de laps, límites, etc.).

---

### 4. Diseño de la Interfaz de Usuario (UI/UX) - Flujo Principal

1.  **Pantalla de Configuración (Opcional al inicio):**
    * El usuario elige el modo: Infinito, Predefinido o Máximo.
    * Si es Predefinido, aparece una lista para que ingrese el nombre de cada subevento.
    * Si es Máximo, un campo numérico para establecer el límite.
    * Un botón "Iniciar Sesión" lleva a la pantalla principal.

2.  **Pantalla Principal del Cronómetro:**
    * **Display grande:** Muestra el tiempo transcurrido en formato `HH:MM:SS.ms`.
    * **Botón principal (cambia de estado):**
        * Estado inicial: **"Iniciar"**.
        * En ejecución: **"Pausar"**.
        * En pausa: **"Reanudar"**.
    * **Botón secundario:**
        * Cuando el cronómetro está detenido: **"Reiniciar"**.
        * Cuando el cronómetro está en ejecución: **"Registrar"** (o el nombre del siguiente subevento predefinido).
    * **Área de Registros:** Una lista que se actualiza en tiempo real cada vez que se presiona "Registrar", mostrando el nombre del lap y su tiempo.

3.  **Pantalla de Historial:**
    * Una lista de todas las `SesionEvento` guardadas, mostrando nombre, fecha y duración total.
    * Permite al usuario tocar una sesión para ver el detalle completo de todos sus `RegistroTiempo`.
    * Ofrece la opción de eliminar sesiones (mediante un deslizamiento o un botón de edición).

---

### 5. Plan de Desarrollo por Fases

1.  **Fase 1: MVP - Núcleo Funcional**
    * Desarrollar el `TimerEngine` con las funciones básicas (iniciar, pausar, reiniciar).
    * Crear la pantalla principal del cronómetro con el display de tiempo y los botones.
    * Implementar la funcionalidad de registro de laps (modo infinito por defecto) y su visualización en tiempo real.

2.  **Fase 2: Configuración de Eventos**
    * Desarrollar la pantalla y la lógica (`EventManager`) para los modos Predefinido y Máximo.
    * Integrar la configuración con la pantalla principal del cronómetro para que se comporte según el modo elegido.

3.  **Fase 3: Persistencia e Historial**
    * Implementar el `StorageService` para guardar y cargar sesiones.
    * Desarrollar la pantalla de Historial para listar las sesiones.
    * Crear la vista de detalle de una sesión.
    * Implementar la funcionalidad de borrado.

4.  **Fase 4: Refinamiento y Pruebas**
    * Pulir la interfaz de usuario y las animaciones.
    * Realizar pruebas exhaustivas de precisión del cronómetro.
    * Probar la fiabilidad de la persistencia de datos (ej: ¿qué pasa si la app se cierra inesperadamente?).
    * Depuración final y preparación para el lanzamiento.

---

### 6. Tecnologías Recomendadas

* **Nativo (iOS):** Swift, SwiftUI para la UI, CoreData o Realm para la persistencia.
* **Nativo (Android):** Kotlin, Jetpack Compose para la UI, Room (SQLite) o Realm para la persistencia.
* **Multiplataforma:** Flutter (con Dart) o React Native (con TypeScript). Ambas opciones son excelentes para este tipo de aplicación y permiten compartir una gran base de código entre iOS y Android. La persistencia se puede manejar con `shared_preferences` o `sqflite` (Flutter) o `AsyncStorage` / `Realm` (React Native).