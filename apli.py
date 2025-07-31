import streamlit as st
import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import DCTERMS, FOAF, XSD, SKOS, OWL
import re

# --- 1. Definición de Namespaces (igual que tu script original) ---
BIBO = Namespace("http://purl.org/ontology/bibo/")
VIVO = Namespace("http://vivoweb.org/ontology/core#")
PRISM = Namespace("http://prismstandard.org/namespaces/basic/2.0/")
CITO = Namespace("http://purl.org/spar/cito/")
SCHEMA = Namespace("http://schema.org/")
EC_RES = Namespace("http://universidades.ec/resource/")

# --- 2. Función de Limpieza (igual que tu script original) ---
def normalize_text_for_uri(text):
    """Limpia y normaliza un string para que sea una URI válida."""
    if pd.isna(text):
        return None
    text = str(text).lower().strip()
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text

# --- 3. Lógica de Conversión Adaptada a una Función ---
# Esta es la parte más importante: tu lógica de conversión ahora está en una función
# que recibe el DataFrame y la configuración de mapeo desde la interfaz de Streamlit.
def convert_csv_to_rdf(df, column_mapping):
    """
    Convierte un DataFrame de Pandas a un grafo RDF según el mapeo de columnas.
    
    Args:
        df (pd.DataFrame): El DataFrame con los datos del CSV.
        column_mapping (dict): Un diccionario que mapea roles a nombres de columnas.
                               Ej: {'DOI': 'DOI', 'Title': 'Article Title', ...}
    
    Returns:
        str: El grafo RDF serializado en formato Turtle.
    """
    g = Graph()
    g.bind("dcterms", DCTERMS)
    g.bind("foaf", FOAF)
    g.bind("bibo", BIBO)
    g.bind("skos", SKOS)
    g.bind("vivo", VIVO)
    g.bind("prism", PRISM)
    g.bind("cito", CITO)
    g.bind("schema", SCHEMA)
    g.bind("owl", OWL)
    g.bind("res", EC_RES)

    processed_rows = 0
    errors = []

    # Iteramos sobre las filas del DataFrame
    for index, row in df.iterrows():
        try:
            # --- Validación de Fila: Saltamos filas si el ID principal (DOI) no existe ---
            doi_col = column_mapping.get('DOI')
            author_id_col = column_mapping.get('Author(s) ID')
            
            if not doi_col or pd.isna(row[doi_col]) or not author_id_col or pd.isna(row[author_id_col]):
                continue

            # --- A. Creación del Recurso Publicación ---
            doi_clean = row[doi_col].strip()
            publication_uri = EC_RES[f"publication/{normalize_text_for_uri(doi_clean)}"]

            # --- B. Asignación de Tipo de Documento ---
            doc_type_col = column_mapping.get('Document Type')
            if doc_type_col and pd.notna(row[doc_type_col]):
                doc_type = str(row[doc_type_col]).lower()
                if 'book chapter' in doc_type:
                    g.add((publication_uri, RDF.type, BIBO.BookChapter))
                elif 'review' in doc_type:
                    g.add((publication_uri, RDF.type, BIBO.Review))
                else:
                    g.add((publication_uri, RDF.type, BIBO.Article))
            else:
                 g.add((publication_uri, RDF.type, BIBO.Article)) # Default

            # --- C. Añadir Propiedades y Metadatos ---
            # Mapeamos cada propiedad a su columna correspondiente si existe
            # Esta es la nueva lógica flexible que usa el mapeo de la UI
            prop_map = {
                DCTERMS.title: 'Title', BIBO.doi: 'DOI', BIBO.eid: 'EID', SCHEMA.url: 'Link',
                DCTERMS.created: 'Year', CITO.isCitedByCount: 'Cited by', DCTERMS.isPartOf: 'Source title',
                BIBO.volume: 'Volume', BIBO.issue: 'Issue', BIBO.number: 'Art. No.',
                BIBO.pageStart: 'Page start', BIBO.pageEnd: 'Page end'
            }
            
            for prop, role in prop_map.items():
                col_name = column_mapping.get(role)
                if col_name and pd.notna(row[col_name]):
                    value = row[col_name]
                    if prop == DCTERMS.created:
                        g.add((publication_uri, prop, Literal(value, datatype=XSD.gYear)))
                    elif prop == CITO.isCitedByCount:
                        g.add((publication_uri, prop, Literal(int(value), datatype=XSD.integer)))
                    elif prop == SCHEMA.url:
                        g.add((publication_uri, prop, URIRef(value)))
                    elif prop == DCTERMS.isPartOf:
                         source_uri = EC_RES[f"source/{normalize_text_for_uri(value)}"]
                         g.add((source_uri, RDF.type, BIBO.Journal))
                         g.add((source_uri, DCTERMS.title, Literal(value)))
                         g.add((publication_uri, prop, source_uri))
                    else:
                        g.add((publication_uri, prop, Literal(value)))

            # --- D. Modelo de Palabras Clave ---
            keywords_col = column_mapping.get('Author Keywords')
            if keywords_col and pd.notna(row[keywords_col]):
                keywords = str(row[keywords_col]).split(';')
                for kw in keywords:
                    kw = kw.strip()
                    if kw:
                        keyword_uri = EC_RES[f"keyword/{normalize_text_for_uri(kw)}"]
                        g.add((keyword_uri, RDF.type, SKOS.Concept))
                        g.add((keyword_uri, SKOS.prefLabel, Literal(kw, lang='en')))
                        g.add((publication_uri, DCTERMS.subject, keyword_uri))
            
            # --- E. Modelo de Autoría ---
            author_names_col = column_mapping.get('Author full names')
            
            if author_id_col and pd.notna(row[author_id_col]):
                author_ids = str(row[author_id_col]).split(';')
                author_full_names = str(row.get(author_names_col, '')).split(';')

                for i, author_id in enumerate(author_ids):
                    author_id = author_id.strip()
                    if not author_id: continue

                    author_uri = EC_RES[f"author/{author_id}"]
                    g.add((author_uri, RDF.type, FOAF.Person))
                    g.add((author_uri, OWL.sameAs, URIRef(f"https://www.scopus.com/authid/detail.uri?authorId={author_id}")))

                    if i < len(author_full_names) and author_names_col:
                        match = re.search(r'([^()]+)', author_full_names[i])
                        if match:
                            g.add((author_uri, FOAF.name, Literal(match.group(1).strip())))

                    authorship_uri = EC_RES[f"authorship/{normalize_text_for_uri(doi_clean)}/{author_id}"]
                    g.add((publication_uri, VIVO.relatedBy, authorship_uri))
                    g.add((authorship_uri, RDF.type, VIVO.Authorship))
                    g.add((authorship_uri, VIVO.relates, author_uri))
                    g.add((authorship_uri, VIVO.rank, Literal(i + 1, datatype=XSD.integer)))
            
            processed_rows += 1
        except Exception as e:
            errors.append(f"Fila {index + 2}: {e}")
            continue

    # Serializamos el grafo para devolverlo como texto
    ttl_data = g.serialize(format='turtle')
    return ttl_data, len(g), processed_rows, errors


# --- 4. Interfaz Gráfica con Streamlit ---
st.set_page_config(layout="wide", page_title="CSV a RDF Mapeador")

st.title("️️️🗺️ Mapeador Interactivo de CSV a RDF")
st.markdown("Sube tu archivo CSV, mapea las columnas a propiedades semánticas y genera un archivo RDF (Turtle).")

# Opciones de mapeo que el usuario puede elegir
# Estas son las claves que busca la función de conversión
MAPPING_OPTIONS = [
    "Ignorar", "DOI", "Title", "Author(s) ID", "Author full names", "Year",
    "Source title", "Volume", "Issue", "Art. No.", "Page start", "Page end",
    "Cited by", "Link", "EID", "Document Type", "Author Keywords"
]

# Inicializar st.session_state para guardar los resultados
if 'ttl_output' not in st.session_state:
    st.session_state.ttl_output = ""
    st.session_state.graph_len = 0
    st.session_state.processed_rows = 0
    st.session_state.errors = []


# --- PASO 1: Carga del Archivo ---
st.header("1. Sube tu Archivo CSV")
uploaded_file = st.file_uploader("Selecciona un archivo .csv", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding='utf-8')
        df.columns = df.columns.str.strip()
        st.success(f"Archivo '{uploaded_file.name}' cargado con éxito. Se encontraron {len(df)} filas.")
        
        # --- PASO 2: Configuración del Mapeo ---
        st.header("2. Configura el Mapeo de Columnas")
        st.markdown("Asigna un rol a cada columna de tu CSV. La herramienta intentará adivinar el mejor mapeo.")

        mapping_config = {}
        csv_columns = df.columns.tolist()

        # Usamos columnas para un layout más limpio
        cols = st.columns(3)
        col_index = 0

        for column in csv_columns:
            # Intenta adivinar la opción correcta
            suggested_index = 0 # 'Ignorar' por defecto
            for i, option in enumerate(MAPPING_OPTIONS):
                if option.lower().replace(" ", "") in column.lower().replace(" ", ""):
                    suggested_index = i
                    break

            with cols[col_index % 3]:
                selected_option = st.selectbox(
                    f"Columna: **{column}**",
                    options=MAPPING_OPTIONS,
                    index=suggested_index,
                    key=f"map_{column}"
                )
            
            if selected_option != "Ignorar":
                mapping_config[selected_option] = column
            
            col_index += 1

        # --- PASO 3: Generación del Archivo ---
        st.header("3. Generar Archivo TTL")
        
        if st.button("🚀 Generar TTL", type="primary"):
            with st.spinner("Convirtiendo... Este proceso puede tardar unos segundos."):
                ttl_data, graph_len, processed, errors = convert_csv_to_rdf(df, mapping_config)
                st.session_state.ttl_output = ttl_data
                st.session_state.graph_len = graph_len
                st.session_state.processed_rows = processed
                st.session_state.errors = errors
        
        # --- PASO 4: Resultados ---
        if st.session_state.ttl_output:
            st.header("4. Resultado Generado")
            st.success(f"¡Conversión exitosa! Se procesaron **{st.session_state.processed_rows} filas** y se generaron **{st.session_state.graph_len} triples RDF**.")
            
            st.code(st.session_state.ttl_output, language='turtle')
            
            st.download_button(
                label="📥 Descargar Archivo .ttl",
                data=st.session_state.ttl_output,
                file_name="transformado.ttl",
                mime="text/turtle"
            )

            if st.session_state.errors:
                with st.expander("Ver advertencias de procesamiento"):
                    st.warning(f"Se encontraron {len(st.session_state.errors)} problemas al procesar las filas:")
                    for error in st.session_state.errors:
                        st.text(error)

    except Exception as e:
        st.error(f"Error al procesar el archivo CSV: {e}")
