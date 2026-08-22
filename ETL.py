from email.utils import parseaddr, parsedate_to_datetime
import base64
import pandas as pd
import pyodbc
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
credentials_path = os.path.join(BASE_DIR, "credentials.json")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def conectar_sql():

    conn = pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=LAPTOP-DR8C1BKS\\MSSQLSERVER01;"
        "DATABASE=Pipeline_gmail;"
        "Trusted_Connection=yes;"
    )

    return conn

def cargar_sql(df):

    conn = conectar_sql()
    cursor = conn.cursor()

    try:

        for _, fila in df.iterrows():

            cursor.execute(
                """
                INSERT INTO dbo.gmail_correos
                (
                    Id_correo,
                    Fecha,
                    Nombre_Remitente,
                    Email_Remitente,
                    Asunto
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                fila["id_correo"],
                fila["fecha"].to_pydatetime(),
                fila["nombre_remitente"],
                fila["email_remitente"],
                fila["asunto"]
            )

        conn.commit()

        print("Carga realizada correctamente.")

        return len(df)

    except Exception as e:

        conn.rollback()

        print("Error durante la carga:", e)

    finally:

        cursor.close()
        conn.close()

def registrar_log(
    fecha_ejecucion,
    correos_encontrados,
    correos_existentes,
    correos_nuevos,
    estado,
    mensaje_error=None
):

    conn = conectar_sql()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO dbo.etl_log
        (
            fecha_ejecucion,
            correos_encontrados,
            correos_existentes,
            correos_nuevos,
            estado,
            mensaje_error
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        fecha_ejecucion,
        correos_encontrados,
        correos_existentes,
        correos_nuevos,
        estado,
        mensaje_error
    )

    conn.commit()

    cursor.close()
    conn.close()

#consultar IDs existentes en la base de datos para evitar duplicados
def obtener_ids_existentes():

    conn = conectar_sql()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT Id_correo
        FROM dbo.gmail_correos
    """)

    ids = {fila[0] for fila in cursor.fetchall()}

    cursor.close()
    conn.close()

    return ids

def conectar_gmail():

    creds = None

    carpeta_proyecto = os.path.dirname(os.path.abspath(__file__))

    token_path = os.path.join(
        carpeta_proyecto,
        "token.json"
    )

    # Si ya existe una sesión autorizada
    if os.path.exists(token_path):

        creds = Credentials.from_authorized_user_file(
            token_path,
            SCOPES
        )

    # Si no existe o expiró
    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path,
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        # Guardamos el token en la carpeta del proyecto
        with open(token_path, "w") as token:

            token.write(creds.to_json())

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    return service

def obtener_correos(service):

    correos = []
    page_token = None
    max_paginas = 3

    pagina = 0

    while pagina < max_paginas:

        resultado = service.users().messages().list(
            userId="me",
            maxResults=10,
            pageToken=page_token
        ).execute()

        mensajes = resultado.get("messages", [])

        pagina += 1

        print(f"Página {pagina}: {len(mensajes)} mensajes")

        for mensaje in mensajes:

            correo = service.users().messages().get(
                userId="me",
                id=mensaje["id"],
                format="full"
            ).execute()

            correos.append(correo)

        page_token = resultado.get("nextPageToken")

        if not page_token:
            break

    print("Total de correos obtenidos:", len(correos))

    return correos

def extraer_datos(correo):

    headers = correo["payload"]["headers"]

    datos = {}

    for header in headers:

        nombre = header["name"]
        valor = header["value"]

        if nombre == "From":

            nombre_remitente, email_remitente = parseaddr(valor)

            datos["nombre_remitente"] = nombre_remitente
            datos["email_remitente"] = email_remitente

        elif nombre == "Subject":

            datos["asunto"] = valor

        elif nombre == "Date":

            datos["fecha"] = parsedate_to_datetime(valor)

    datos["id_correo"] = correo["id"]

    return datos

def main():
   
  try:

    print("Conectando con Gmail...")

    service = conectar_gmail()

    print("Conexión exitosa.")


    correos = obtener_correos(service)

    print(f"Correos encontrados: {len(correos)}")

    datos_correos = []

    for correo in correos:

        print("Procesando correo...")

        datos = extraer_datos(correo)

        print("Correo procesado:", datos)

        datos_correos.append(datos)

    print("Terminó la extracción.")

    df = pd.DataFrame(datos_correos)

    df["fecha"] = pd.to_datetime(df["fecha"], utc=True)

    ids_existentes = obtener_ids_existentes()

    df_nuevos = df[
        ~df["id_correo"].isin(ids_existentes)
    ]

    correos_encontrados = len(df)

    correos_existentes = len(
        df[df["id_correo"].isin(ids_existentes)]
    )

    correos_nuevos = len(df_nuevos)

    print("\nCorreos encontrados en Gmail:", correos_encontrados)

    print("Correos ya existentes:", correos_existentes)

    print("Correos nuevos:", correos_nuevos)

    print(df)

    print("\nCOLUMNAS:")
    print(df.columns)

    print("\nTIPOS DE DATOS:")
    print(df.dtypes)

    print("\nVALORES NULOS:")
    print(df.isnull().sum())

    print("\nCANTIDAD DE CORREOS NUEVOS:", len(df_nuevos))

    print("¿DF_NUEVOS ESTÁ VACÍO?:", df_nuevos.empty)

    if not df_nuevos.empty:

        cantidad_insertada = cargar_sql(df_nuevos)

        print("Nuevos correos cargados:", cantidad_insertada)

    else:

        print("No hay correos nuevos para cargar.")

    registrar_log(
        datetime.now(),
        correos_encontrados,
        correos_existentes,
        correos_nuevos,
        "OK"
    )

    print("Ejecución registrada en etl_log.")

    print("Datos cargados correctamente en SQL Server.")

    print("\nCORREOS DUPLICADOS:")
    print(df["id_correo"].duplicated().sum())
    print("FIN DEL PIPELINE")

  except Exception as e:
    print("ERROR EN EL PIPELINE:", e)

    registrar_log(
        datetime.now(),
        0,
        0,
        0,
        "ERROR",
        str(e)
    )

if __name__ == "__main__":
    main()
