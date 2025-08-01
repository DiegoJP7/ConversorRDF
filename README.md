Mapeador Semántico Interactivo: CSV a RDF
Una aplicación web desarrollada con Streamlit y Python que permite a los usuarios transformar datos tabulares (desde un archivo CSV) en un grafo de conocimiento RDF en formato Turtle. La herramienta ofrece una interfaz gráfica intuitiva para mapear columnas de un CSV a propiedades semánticas de ontologías conocidas (BIBO, FOAF, SKOS, etc.), democratizando la creación de datos enlazados.
(Recomendación: Reemplaza la siguiente línea con una captura de pantalla o un GIF de tu aplicación en funcionamiento. Puedes subir la imagen a tu repositorio de GitHub y enlazarla)
![Demo de la Aplicación](URL_DE_TU_IMAGEN_O_GIF_AQUI)
🚀 Características Principales
Interfaz Web Interactiva: Una experiencia de usuario limpia y fácil de usar construida con Streamlit.
Carga de Archivos Simplificada: Sube tu archivo CSV directamente desde el navegador.
Mapeo Inteligente: Asigna de forma flexible cada columna de tu CSV a una propiedad semántica RDF. La herramienta sugiere mapeos probables.
Generación "One-Click": Crea el grafo de conocimiento en formato Turtle (.ttl) con un solo botón.
Visualización y Descarga: Revisa el resultado directamente en la aplicación y descárgalo para usarlo en otros sistemas.
🛠️ Prerrequisitos
Antes de comenzar, asegúrate de tener instalado en tu sistema:
Python 3.8 o superior
pip (el gestor de paquetes de Python)
⚙️ Instalación y Puesta en Marcha
Sigue estos pasos en tu terminal para configurar y ejecutar el proyecto localmente.
1. Clona el repositorio:
(No olvides cambiar la URL por la de tu propio repositorio)
git clone https://github.com/tu-usuario/tu-repositorio.git


2. Navega al directorio del proyecto:
cd tu-repositorio


3. (Recomendado) Crea y activa un entorno virtual:
Crear el entorno:
python -m venv venv


Activar en Windows:
venv\Scripts\activate


Activar en macOS/Linux:
source venv/bin/activate


4. Crea el archivo requirements.txt:
Crea un archivo llamado requirements.txt en la raíz del proyecto y añade las siguientes librerías:
streamlit
pandas
rdflib


5. Instala las dependencias:
Con tu entorno virtual activo, instala todas las librerías necesarias con un solo comando:
pip install -r requirements.txt


▶️ Uso de la Aplicación
Una vez que todas las dependencias estén instaladas, puedes iniciar la aplicación con el siguiente comando:
streamlit run app.py


Tu navegador web se abrirá automáticamente en una nueva pestaña, mostrando la aplicación en http://localhost:8501.
Salida Esperada
La aplicación te dará la bienvenida y te pedirá que subas un archivo CSV.
Una vez cargado, se mostrará una interfaz para que mapees cada columna del CSV a una propiedad RDF.
Después de configurar el mapeo y hacer clic en el botón "Generar TTL", la aplicación procesará el archivo.
Finalmente, verás un área de texto con el código Turtle (.ttl) generado y un botón para descargar el archivo resultante.
📂 Estructura del Proyecto
.
├── app.py          # Script principal que contiene la lógica y la interfaz de Streamlit.
├── requirements.txt # Lista de dependencias de Python para una fácil instalación.
└── README.md       # Este archivo de documentación.


🧠 ¿Cómo Funciona? (Lógica de Transformación)
El proceso de conversión sigue un flujo de datos lógico y bien definido:
Ingesta y Preparación: El archivo .csv subido por el usuario es leído y cargado en un DataFrame de Pandas. Esto permite una manipulación de datos eficiente y robusta.
Mapeo Semántico: A través de la interfaz de Streamlit, el usuario define un diccionario de reglas que conecta las columnas del DataFrame con las URIs de las propiedades de ontologías estándar (ej. dcterms:title).
Construcción del Grafo: El script itera sobre cada fila del DataFrame. Usando las reglas de mapeo, instancia recursos RDF (nodos) y crea las conexiones entre ellos (tripletas) con la librería RDFLib.
Serialización: Una vez que todas las filas han sido procesadas, el grafo RDF completo en memoria es "serializado", es decir, convertido a una representación textual en formato Turtle (.ttl), que es legible tanto para humanos como para máquinas.
