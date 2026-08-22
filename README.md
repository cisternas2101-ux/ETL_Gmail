# 📧 ETL Gmail Data Pipeline

Pipeline ETL desarrollado en **Python** para extraer información de correos electrónicos desde Gmail mediante la **Gmail API**, transformar los datos y almacenarlos en **SQL Server** para su posterior análisis y visualización mediante un dashboard interactivo en **Streamlit**.

El proyecto fue desarrollado como una solución práctica de integración, automatización y monitoreo de datos.

---

## 🏗️ Arquitectura

```text
┌──────────────┐
│    Gmail     │
│     API      │
└──────┬───────┘
       │
       │ Extracción
       ▼
┌──────────────┐
│    Python    │
│    ETL.py    │
└──────┬───────┘
       │
       │ Transformación
       │ Validación
       │ Control de duplicados
       ▼
┌──────────────┐
│  SQL Server  │
│ gmail_correos│
└──────┬───────┘
       │
       │ Consultas SQL
       ▼
┌──────────────┐
│  Streamlit   │
│  Dashboard   │
└──────────────┘
```

---

## 🎯 Objetivo del proyecto

Construir un pipeline capaz de:

* Conectarse a Gmail mediante una API.
* Extraer información de correos electrónicos.
* Procesar y transformar los datos utilizando Python.
* Detectar correos ya existentes.
* Insertar únicamente nuevos registros.
* Registrar las ejecuciones del proceso ETL.
* Almacenar la información estructurada en SQL Server.
* Visualizar los datos mediante un dashboard interactivo.
* Monitorear el estado y rendimiento de las ejecuciones.

---

## 🛠️ Tecnologías utilizadas

| Tecnología           | Uso                                    |
| -------------------- | -------------------------------------- |
| **Python**           | Desarrollo del proceso ETL             |
| **Gmail API**        | Extracción de información desde Gmail  |
| **Google OAuth 2.0** | Autenticación y autorización           |
| **SQL Server**       | Almacenamiento y consulta de datos     |
| **pyodbc**           | Conexión entre Python y SQL Server     |
| **Pandas**           | Manipulación y transformación de datos |
| **Streamlit**        | Desarrollo del dashboard               |
| **Plotly**           | Visualización de datos                 |
| **Git**              | Control de versiones                   |
| **GitHub**           | Repositorio y publicación del proyecto |

---

## 📂 Estructura del proyecto

```text
ETL_Gmail/
│
├── ETL.py
├── dashboard.py
├── .gitignore
└── README.md
```

### `ETL.py`

Contiene el proceso ETL principal:

1. Autenticación con Gmail.
2. Conexión con Gmail API.
3. Extracción de correos.
4. Lectura de información relevante.
5. Transformación de datos.
6. Validación de registros existentes.
7. Inserción de nuevos registros en SQL Server.
8. Registro de la ejecución del proceso.
9. Control de errores.

### `dashboard.py`

Contiene el dashboard desarrollado con Streamlit para consultar y analizar la información almacenada en SQL Server.

---

## 📊 Datos almacenados

La información principal de los correos se almacena en la tabla:

```text
dbo.gmail_correos
```

Principales campos:

| Campo              | Descripción                               |
| ------------------ | ----------------------------------------- |
| `Id_correo`        | Identificador único del correo            |
| `Fecha`            | Fecha y hora del correo                   |
| `Nombre_Remitente` | Nombre del remitente                      |
| `Email_Remitente`  | Dirección de correo del remitente         |
| `Asunto`           | Asunto del correo                         |
| `Fecha_Carga`      | Fecha de carga del registro en SQL Server |

El campo `Id_correo` se utiliza como identificador único para evitar duplicados.

---

## 🔄 Proceso ETL

### 1. Extract

El proceso se conecta a Gmail utilizando la Gmail API y obtiene información de los correos disponibles.

La autenticación utiliza OAuth 2.0.

### 2. Transform

Los datos obtenidos son procesados mediante Python y Pandas.

Durante esta etapa se realizan tareas como:

* Normalización de información.
* Conversión de fechas.
* Extracción del nombre y correo del remitente.
* Preparación de los datos para SQL Server.
* Validación de registros.
* Control de duplicados.

### 3. Load

Los registros son almacenados en SQL Server.

Antes de insertar un correo, el proceso verifica si el identificador ya existe en la base de datos.

De esta manera, el pipeline permite realizar ejecuciones periódicas sin generar registros duplicados.

---

## 🗄️ Control de ejecuciones

El proyecto también incorpora un mecanismo de seguimiento de las ejecuciones del ETL.

Se registran datos como:

* Fecha de ejecución.
* Cantidad de correos encontrados.
* Cantidad de correos existentes.
* Cantidad de correos nuevos.
* Estado de la ejecución.
* Mensaje de error cuando corresponde.

Esto permite monitorear el funcionamiento del pipeline y detectar ejecuciones fallidas.

---

## 📈 Dashboard

El dashboard fue desarrollado utilizando **Streamlit** y permite analizar la información almacenada en SQL Server.

Entre los principales indicadores se encuentran:

* 📧 Total de correos.
* 📊 Correos únicos.
* 👤 Remitentes únicos.
* ⚙️ Cantidad de ejecuciones ETL.
* ✅ Ejecuciones exitosas.
* ❌ Ejecuciones con error.
* 🕐 Última ejecución.
* 📅 Correos recibidos por día.
* ⏰ Correos recibidos por hora.
* 👤 Correos por remitente.
* 🌐 Correos por dominio.

También permite aplicar filtros y descargar información para análisis posterior.

---

## ⚙️ Configuración

### Requisitos

Se requiere tener instalado:

* Python 3.10+
* SQL Server
* Git
* Una cuenta de Google con acceso a Gmail API

### Dependencias principales

```bash
pip install google-api-python-client
pip install google-auth
pip install google-auth-oauthlib
pip install pyodbc
pip install pandas
pip install streamlit
pip install plotly
```

También puedes instalar las dependencias desde un archivo `requirements.txt` si posteriormente se incorpora al proyecto.

---

## 🔐 Configuración de Gmail API

Para ejecutar el proyecto es necesario configurar un proyecto en Google Cloud y habilitar:

```text
Gmail API
```

La autenticación se realiza mediante OAuth 2.0.

Los archivos de credenciales y tokens **no deben ser publicados en GitHub**.

Ejemplos de archivos que deben permanecer fuera del repositorio:

```text
credentials.json
token.json
.env
```

Estos archivos deben estar incluidos en `.gitignore`.

---

## 🗃️ Configuración de SQL Server

El proyecto utiliza SQL Server como base de datos.

La conexión debe configurarse de acuerdo con el entorno local donde se ejecuta el proyecto.

Ejemplo conceptual:

```text
Python
   │
   ▼
pyodbc
   │
   ▼
SQL Server
   │
   ▼
Pipeline_gmail
```

Las credenciales de conexión no deben almacenarse directamente dentro del código fuente.

Se recomienda utilizar variables de entorno mediante un archivo `.env`.

---

## ▶️ Ejecución del ETL

Desde la carpeta del proyecto:

```bash
python ETL.py
```

El proceso realizará la extracción desde Gmail y posteriormente cargará los nuevos registros en SQL Server.

---

## 📊 Ejecución del Dashboard

Para iniciar Streamlit:

```bash
streamlit run dashboard.py
```

Luego se puede acceder al dashboard desde el navegador mediante la dirección proporcionada por Streamlit.

---

## 🔎 Ejemplo del flujo de datos

```text
Correo recibido en Gmail
          │
          ▼
      Gmail API
          │
          ▼
       Python
          │
          ▼
   Transformación
          │
          ▼
Validación de duplicados
          │
          ▼
      SQL Server
          │
          ▼
       Streamlit
          │
          ▼
      Dashboard
```

---

## 📌 Características principales

* Integración con Gmail API.
* Autenticación mediante OAuth 2.0.
* Extracción automatizada de datos.
* Transformación de información mediante Python.
* Persistencia en SQL Server.
* Control de duplicados.
* Registro de ejecuciones ETL.
* Manejo de errores.
* Dashboard interactivo.
* Filtros para análisis.
* Visualizaciones con Plotly.
* Exportación de datos.
* Control de versiones mediante Git.
* Publicación del proyecto en GitHub.

---

## 🚀 Próximas mejoras

Algunas mejoras planificadas para futuras versiones:

* [ ] Incorporar `requirements.txt`.
* [ ] Mejorar la gestión de configuración mediante variables de entorno.
* [ ] Incorporar logging estructurado.
* [ ] Implementar pruebas automatizadas.
* [ ] Incorporar Docker.
* [ ] Migrar la base de datos hacia Azure SQL.
* [ ] Automatizar el despliegue.
* [ ] Incorporar CI/CD mediante GitHub Actions.
* [ ] Mejorar el monitoreo del pipeline.
* [ ] Incorporar nuevas fuentes de datos.

---

## 💡 Aprendizajes

Este proyecto permitió aplicar conceptos relacionados con:

* Procesos ETL.
* Integración de APIs.
* Autenticación OAuth 2.0.
* Python para ingeniería de datos.
* Manipulación de datos con Pandas.
* SQL y SQL Server.
* Automatización de procesos.
* Control de duplicados.
* Manejo de errores.
* Monitoreo de pipelines.
* Visualización de datos.
* Git y GitHub.

---

## 👩‍💻 Proyecto

**ETL Gmail Data Pipeline**

Desarrollado como proyecto práctico de **Data Engineering**, integrando extracción, transformación, almacenamiento, automatización y visualización de datos.

---

## 📄 Licencia

Este proyecto se encuentra disponible para fines educativos y de portfolio profesional.
