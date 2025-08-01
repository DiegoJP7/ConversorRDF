# Mapeador Semántico Interactivo: CSV a RDF

Una aplicación web desarrollada con Streamlit y Python que permite a los usuarios transformar datos tabulares (desde un archivo CSV) en un grafo de conocimiento RDF en formato Turtle. La herramienta ofrece una interfaz gráfica intuitiva para mapear columnas de un CSV a propiedades semánticas de ontologías conocidas (BIBO, FOAF, SKOS, etc.), democratizando la creación de datos enlazados.

---

## 🚀 Características Principales

-   **Interfaz Web Interactiva:** Una experiencia de usuario limpia y fácil de usar construida con Streamlit.
-   **Carga de Archivos Simplificada:** Sube tu archivo CSV directamente desde el navegador.
-   **Mapeo Inteligente:** Asigna de forma flexible cada columna de tu CSV a una propiedad semántica RDF. La herramienta sugiere mapeos probables.
-   **Generación "One-Click":** Crea el grafo de conocimiento en formato Turtle (`.ttl`) con un solo botón.
-   **Visualización y Descarga:** Revisa el resultado directamente en la aplicación y descárgalo para usarlo en otros sistemas.

---

## 🛠️ Prerrequisitos

Antes de comenzar, asegúrate de tener instalado en tu sistema:

-   **Python 3.8** o superior
-   **pip** (el gestor de paquetes de Python)

---

# Mapeador Semántico Interactivo: CSV a RDF

Aplicación web que transforma archivos CSV de publicaciones científicas a un grafo de conocimiento RDF (`.ttl`). Permite mapear las columnas del CSV a propiedades semánticas de forma visual.

---

## 🛠️ Requisitos

* **Python 3.8** o superior
* **pip** (el gestor de paquetes de Python)

---

## ⚙️ Instalación

Abre tu terminal y sigue estos pasos:

**1. Clona el repositorio:**
*(Recuerda cambiar la URL por la de tu repositorio)*
```bash
git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
```
**2. Entra a la carpeta del proyecto:**
```bash
cd tu-repositorio
```
**3. Instala las librerías necesarias:**
```bash
pip install streamlit pandas rdflib
```
**▶️ Cómo Ejecutar**
Una vez instalado todo, ejecuta este comando en tu terminal:
```bash
streamlit run app.py
```
