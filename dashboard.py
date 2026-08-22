import streamlit as st
import pyodbc
import pandas as pd
import plotly.express as px


# ============================================================
# CONFIGURACIÓN DE STREAMLIT
# ============================================================

st.set_page_config(
    page_title="Gmail Data Pipeline",
    page_icon="📧",
    layout="wide"
)


# ============================================================
# TÍTULO
# ============================================================

st.title("📧 Gmail Jennifer Data Pipeline")
st.write("Dashboard de monitoreo del ETL de Gmail")


# ============================================================
# BOTÓN ACTUALIZAR
# ============================================================

if st.button("🔄 Actualizar datos"):
    st.rerun()


# ============================================================
# CONEXIÓN SQL SERVER
# ============================================================

def conectar_sql():

    conn = pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=LAPTOP-DR8C1BKS\\MSSQLSERVER01;"
        "DATABASE=Pipeline_gmail;"
        "Trusted_Connection=yes;"
    )

    return conn

# ============================================================
# RANGO DE FECHAS DISPONIBLE
# ============================================================

def obtener_rango_fechas():

    conn = conectar_sql()

    consulta = """
        SELECT
            MIN(CAST(Fecha AS DATE)) AS fecha_minima,
            MAX(CAST(Fecha AS DATE)) AS fecha_maxima
        FROM dbo.gmail_correos
    """

    df = pd.read_sql(
        consulta,
        conn
    )

    conn.close()

    return df


# ============================================================
# OBTENER REMITENTES
# ============================================================

def obtener_remitentes():

    conn = conectar_sql()

    consulta = """
        SELECT DISTINCT
            Nombre_Remitente
        FROM dbo.gmail_correos
        ORDER BY Nombre_Remitente
    """

    df = pd.read_sql(
        consulta,
        conn
    )

    conn.close()

    return df["Nombre_Remitente"].tolist()


# ============================================================
# RESUMEN / KPIs
# ============================================================

def obtener_resumen_filtrado(
    fecha_inicio,
    fecha_fin,
    remitente,
    asunto
):

    conn = conectar_sql()

    consulta = """
        SELECT
            COUNT(*) AS total_correos,
            COUNT(DISTINCT Id_correo) AS correos_unicos,
            COUNT(DISTINCT Email_Remitente) AS remitentes_unicos
        FROM dbo.gmail_correos
        WHERE CAST(Fecha AS DATE) BETWEEN ? AND ?
        AND (? = 'Todos' OR Nombre_Remitente = ?)
        AND (? = '' OR Asunto LIKE ?)
    """

    texto_asunto = f"%{asunto}%"

    df = pd.read_sql(
        consulta,
        conn,
        params=[
            str(fecha_inicio),
            str(fecha_fin),
            remitente,
            remitente,
            asunto,
            texto_asunto
        ]
    )

    conn.close()

    return df

# ============================================================
# CORREOS FILTRADOS
# ============================================================

def obtener_correos_filtrados(
    fecha_inicio,
    fecha_fin,
    remitente,
    asunto
):

    conn = conectar_sql()

    consulta = """
        SELECT
            Id_correo,
            Fecha,
            Nombre_Remitente,
            Email_Remitente,
            Asunto
        FROM dbo.gmail_correos
        WHERE CAST(Fecha AS DATE) BETWEEN ? AND ?
        AND (? = 'Todos' OR Nombre_Remitente = ?)
        AND (? = '' OR Asunto LIKE ?)
        ORDER BY Fecha DESC
    """

    texto_asunto = f"%{asunto}%"

    df = pd.read_sql(
        consulta,
        conn,
        params=[
            str(fecha_inicio),
            str(fecha_fin),
            remitente,
            remitente,
            asunto,
            texto_asunto
        ]
    )

    conn.close()

    return df


# ============================================================
# CORREOS POR DÍA
# ============================================================

def obtener_correos_por_dia_filtrado(
    fecha_inicio,
    fecha_fin,
    remitente,
    asunto
):

    conn = conectar_sql()

    consulta = """
        SELECT
            CAST(Fecha AS DATE) AS fecha,
            COUNT(*) AS cantidad_correos
        FROM dbo.gmail_correos
        WHERE CAST(Fecha AS DATE) BETWEEN ? AND ?
        AND (? = 'Todos' OR Nombre_Remitente = ?)
        AND (? = '' OR Asunto LIKE ?)
        GROUP BY CAST(Fecha AS DATE)
        ORDER BY fecha
    """

    texto_asunto = f"%{asunto}%"

    df = pd.read_sql(
        consulta,
        conn,
        params=[
            str(fecha_inicio),
            str(fecha_fin),
            remitente,
            remitente,
            asunto,
            texto_asunto
        ]
    )

    conn.close()

    return df


# ============================================================
# CORREOS POR HORA
# ============================================================

def obtener_correos_por_hora_filtrado(
    fecha_inicio,
    fecha_fin,
    remitente,
    asunto
):

    conn = conectar_sql()

    consulta = """
        SELECT
            DATEPART(HOUR, Fecha) AS hora,
            COUNT(*) AS cantidad_correos
        FROM dbo.gmail_correos
        WHERE CAST(Fecha AS DATE) BETWEEN ? AND ?
        AND (? = 'Todos' OR Nombre_Remitente = ?)
        AND (? = '' OR Asunto LIKE ?)
        GROUP BY DATEPART(HOUR, Fecha)
        ORDER BY hora
    """

    texto_asunto = f"%{asunto}%"

    df = pd.read_sql(
        consulta,
        conn,
        params=[
            str(fecha_inicio),
            str(fecha_fin),
            remitente,
            remitente,
            asunto,
            texto_asunto
        ]
    )

    conn.close()

    return df

# ============================================================
# CORREOS POR REMITENTE
# ============================================================

def obtener_correos_por_remitente_filtrado(
    fecha_inicio,
    fecha_fin,
    remitente,
    asunto
):

    conn = conectar_sql()

    consulta = """
        SELECT
            Nombre_Remitente,
            COUNT(*) AS cantidad_correos
        FROM dbo.gmail_correos
        WHERE CAST(Fecha AS DATE) BETWEEN ? AND ?
        AND (? = 'Todos' OR Nombre_Remitente = ?)
        AND (? = '' OR Asunto LIKE ?)
        GROUP BY Nombre_Remitente
        ORDER BY cantidad_correos DESC
    """

    texto_asunto = f"%{asunto}%"

    df = pd.read_sql(
        consulta,
        conn,
        params=[
            str(fecha_inicio),
            str(fecha_fin),
            remitente,
            remitente,
            asunto,
            texto_asunto
        ]
    )

    conn.close()

    return df
# ============================================================
# ÚLTIMOS CORREOS
# ============================================================

def obtener_ultimos_correos(
    fecha_inicio,
    fecha_fin,
    remitente,
    asunto
):

    conn = conectar_sql()

    consulta = """
        SELECT
            Fecha,
            Nombre_Remitente,
            Email_Remitente,
            Asunto
        FROM dbo.gmail_correos
        WHERE CAST(Fecha AS DATE) BETWEEN ? AND ?
        AND (? = 'Todos' OR Nombre_Remitente = ?)
        AND (? = '' OR Asunto LIKE ?)
        ORDER BY Fecha DESC
    """

    texto_asunto = f"%{asunto}%"

    df = pd.read_sql(
        consulta,
        conn,
        params=[
            str(fecha_inicio),
            str(fecha_fin),
            remitente,
            remitente,
            asunto,
            texto_asunto
        ]
    )

    conn.close()

    return df

# ============================================================
# ÚLTIMA EJECUCIÓN DEL ETL
# ============================================================

def obtener_ultima_ejecucion():

    conn = conectar_sql()

    consulta = """
        SELECT TOP 1
            id_ejecucion,
            fecha_ejecucion,
            correos_encontrados,
            correos_existentes,
            correos_nuevos,
            estado,
            mensaje_error
        FROM dbo.etl_log
        ORDER BY fecha_ejecucion DESC
    """

    df = pd.read_sql(
        consulta,
        conn
    )

    conn.close()

    return df


# ============================================================
# HISTORIAL DEL ETL
# ============================================================

def obtener_historial_etl():

    conn = conectar_sql()

    consulta = """
        SELECT
            id_ejecucion,
            fecha_ejecucion,
            correos_encontrados,
            correos_existentes,
            correos_nuevos,
            estado,
            mensaje_error
        FROM dbo.etl_log
        ORDER BY id_ejecucion
    """

    df = pd.read_sql(
        consulta,
        conn
    )

    conn.close()

    return df


#===========================================================
# Correos por dominio del remitente
#============================================================
def obtener_correos_por_dominio(
    fecha_inicio,
    fecha_fin,
    remitente,
    asunto
):

    conn = conectar_sql()

    consulta = """
        SELECT
            SUBSTRING(
                Email_Remitente,
                CHARINDEX('@', Email_Remitente) + 1,
                LEN(Email_Remitente)
            ) AS dominio,
            COUNT(*) AS cantidad_correos
        FROM dbo.gmail_correos
        WHERE CAST(Fecha AS DATE) BETWEEN ? AND ?
        AND (? = 'Todos' OR Nombre_Remitente = ?)
        AND (? = '' OR Asunto LIKE ?)
        GROUP BY
            SUBSTRING(
                Email_Remitente,
                CHARINDEX('@', Email_Remitente) + 1,
                LEN(Email_Remitente)
            )
        ORDER BY cantidad_correos DESC
    """

    texto_asunto = f"%{asunto}%"

    df = pd.read_sql(
        consulta,
        conn,
        params=[
            str(fecha_inicio),
            str(fecha_fin),
            remitente,
            remitente,
            asunto,
            texto_asunto
        ]
    )

    conn.close()

    return df

#============================================================
#Salud del pipeline
#============================================================
def obtener_salud_pipeline():

    conn = conectar_sql()

    consulta = """
        SELECT
            COUNT(*) AS total_ejecuciones,

            SUM(
                CASE
                    WHEN estado = 'OK' THEN 1
                    ELSE 0
                END
            ) AS ejecuciones_ok,

            SUM(
                CASE
                    WHEN estado = 'ERROR' THEN 1
                    ELSE 0
                END
            ) AS ejecuciones_error,

            MAX(fecha_ejecucion) AS ultima_ejecucion

        FROM dbo.etl_log
    """

    df = pd.read_sql(
        consulta,
        conn
    )

    conn.close()

    return df

# ============================================================
# 📅 FILTROS
# ============================================================

st.subheader("📅 Filtros")

col_fecha1, col_fecha2, col_remitente, col_asunto = st.columns(4)


# ============================================================
# FECHAS AUTOMÁTICAS
# ============================================================

df_rango = obtener_rango_fechas()

fecha_minima = df_rango["fecha_minima"].iloc[0]
fecha_maxima = df_rango["fecha_maxima"].iloc[0]

if pd.isna(fecha_minima):

    fecha_minima = pd.Timestamp.today().date()

else:

    fecha_minima = pd.to_datetime(
        fecha_minima
    ).date()


fecha_maxima = pd.Timestamp.today().date()


fecha_inicio = col_fecha1.date_input(
    "Fecha inicio",
    value=fecha_minima
)


fecha_fin = col_fecha2.date_input(
    "Fecha fin",
    value=fecha_maxima
)


remitentes = obtener_remitentes()


remitente_seleccionado = col_remitente.selectbox(
    "👤 Remitente",
    ["Todos"] + remitentes
)
asunto_busqueda = col_asunto.text_input(
    "🔎 Buscar asunto",
    placeholder="Ej: logística"
)

# ============================================================
# OBTENER DATOS FILTRADOS
# ============================================================

df_filtrado = obtener_correos_filtrados(
    fecha_inicio,
    fecha_fin,
    remitente_seleccionado,
    asunto_busqueda
)

df_resumen_filtrado = obtener_resumen_filtrado(
    fecha_inicio,
    fecha_fin,
    remitente_seleccionado,
    asunto_busqueda
)

# ============================================================
# RESULTADO DEL FILTRO
# ============================================================

st.write(
    f"📧 Correos encontrados en el período: "
    f"**{len(df_filtrado)}**"
)

# ============================================================
# 📥 DESCARGAR RESULTADOS
# ============================================================

csv = df_filtrado.to_csv(
    index=False,
    encoding="utf-8-sig"
)

st.download_button(
    label="📥 Descargar resultados CSV",
    data=csv,
    file_name="correos_filtrados.csv",
    mime="text/csv"
)

# ============================================================
# 📊 KPIs
# ============================================================

st.subheader("📊 Resumen")


col1, col2, col3 = st.columns(3)


col1.metric(
    "📧 Total correos",
    df_resumen_filtrado["total_correos"].iloc[0]
)


col2.metric(
    "🆔 Correos únicos",
    df_resumen_filtrado["correos_unicos"].iloc[0]
)


col3.metric(
    "👤 Remitentes únicos",
    df_resumen_filtrado["remitentes_unicos"].iloc[0]
)

# ============================================================
# 🩺 SALUD DEL PIPELINE
# ============================================================

st.subheader("🩺 Salud del Pipeline")

df_salud = obtener_salud_pipeline()

total_ejecuciones = int(
    df_salud["total_ejecuciones"].iloc[0]
)

ejecuciones_ok = int(
    df_salud["ejecuciones_ok"].iloc[0]
)

ejecuciones_error = int(
    df_salud["ejecuciones_error"].iloc[0]
)

ultima_ejecucion = df_salud[
    "ultima_ejecucion"
].iloc[0]


# ============================================================
# INDICADOR GENERAL
# ============================================================

if ejecuciones_error == 0:

    st.success(
        "🟢 Pipeline saludable — "
        "No existen ejecuciones con error."
    )

else:

    st.warning(
        f"🟡 Pipeline con incidencias — "
        f"{ejecuciones_error} ejecución(es) con error."
    )


# ============================================================
# MÉTRICAS
# ============================================================

col_salud1, col_salud2, col_salud3, col_salud4 = st.columns(4)


col_salud1.metric(
    "⚙️ Ejecuciones",
    total_ejecuciones
)

col_salud2.metric(
    "🟢 Exitosas",
    ejecuciones_ok
)

col_salud3.metric(
    "🔴 Con error",
    ejecuciones_error
)

col_salud4.metric(
    "🕐 Última ejecución",
    str(ultima_ejecucion)
)

# ============================================================
# ⚙️ ESTADO DEL ETL
# ============================================================

st.subheader("📋 Última ejecución")


df_ultima = obtener_ultima_ejecucion()


if not df_ultima.empty:

    ultima = df_ultima.iloc[0]


    if ultima["estado"] == "OK":

        st.success(
            "🟢 Última ejecución exitosa"
        )

    else:

        st.error(
            "🔴 Última ejecución con error"
        )


    col_etl1, col_etl2, col_etl3, col_etl4 = st.columns(4)


    col_etl1.metric(
        "📧 Correos encontrados",
        ultima["correos_encontrados"]
    )


    col_etl2.metric(
        "♻️ Correos existentes",
        ultima["correos_existentes"]
    )


    col_etl3.metric(
        "🆕 Correos nuevos",
        ultima["correos_nuevos"]
    )


    col_etl4.metric(
        "⚙️ Estado",
        ultima["estado"]
    )



    if ultima["estado"] == "ERROR":

        st.error(
            f"Mensaje de error: "
            f"{ultima['mensaje_error']}"
        )


else:

    st.warning(
        "No existen ejecuciones registradas."
    )



# ============================================================
# 📈 CORREOS RECIBIDOS POR DÍA
# ============================================================

st.subheader("📈 Correos recibidos por día")


df_dias = obtener_correos_por_dia_filtrado(
    fecha_inicio,
    fecha_fin,
    remitente_seleccionado,
    asunto_busqueda
)

# Convertir fecha a texto para que Plotly la trate como categoría
df_dias["fecha"] = pd.to_datetime(df_dias["fecha"]).dt.strftime("%d/%m")

fig_dias = px.line(
    df_dias,
    x="fecha",
    y="cantidad_correos",
    markers=True,
    title="Correos recibidos por día",
    labels={
        "fecha": "Fecha",
        "cantidad_correos": "Correos"
    }
)

fig_dias.update_layout(
    xaxis_type="category"
)

st.plotly_chart(
    fig_dias,
    use_container_width=True
)


# ============================================================
# 🕐 Y 📊 GRÁFICOS EN DOS COLUMNAS
# ============================================================

col_grafico1, col_grafico2 = st.columns(2)


# ============================================================
# 🕐 CORREOS POR HORA
# ============================================================

with col_grafico1:

    st.subheader("🕐 Correos por hora")


    df_horas = obtener_correos_por_hora_filtrado(
    fecha_inicio,
    fecha_fin,
    remitente_seleccionado,
    asunto_busqueda
)


    fig_horas = px.bar(
        df_horas,
        x="hora",
        y="cantidad_correos",
        title="Cantidad de correos por hora",
        labels={
            "hora": "Hora del día",
            "cantidad_correos": "Cantidad de correos"
        }
    )


    fig_horas.update_xaxes(
        dtick=1
    )


    st.plotly_chart(
        fig_horas,
        use_container_width=True
    )


# ============================================================
# 📊 CORREOS POR REMITENTE
# ============================================================

with col_grafico2:

    st.subheader("📊 Correos por remitente")


    df_remitentes = obtener_correos_por_remitente_filtrado(
        fecha_inicio,
        fecha_fin,
        remitente_seleccionado,
        asunto_busqueda
    )


    fig_remitentes = px.bar(
        df_remitentes,
        x="cantidad_correos",
        y="Nombre_Remitente",
        orientation="h",
        title="Cantidad de correos por remitente",
        labels={
            "Nombre_Remitente": "Remitente",
            "cantidad_correos": "Cantidad de correos"
        }
    )


    st.plotly_chart(
        fig_remitentes,
        use_container_width=True
    )
# ============================================================
# 🌐 CORREOS POR DOMINIO
# ============================================================

st.subheader("🌐 Correos por dominio del remitente")

df_dominios = obtener_correos_por_dominio(
    fecha_inicio,
    fecha_fin,
    remitente_seleccionado,
    asunto_busqueda
)

fig_dominios = px.bar(
    df_dominios,
    x="cantidad_correos",
    y="dominio",
    orientation="h",
    title="Cantidad de correos por dominio",
    labels={
        "dominio": "Dominio",
        "cantidad_correos": "Cantidad de correos"
    }
)

st.plotly_chart(
    fig_dominios,
    use_container_width=True
)

# ============================================================
# 📬 ÚLTIMOS CORREOS RECIBIDOS
# ============================================================

st.subheader("📬 Últimos correos recibidos")


df_ultimos = obtener_ultimos_correos(
    fecha_inicio,
    fecha_fin,
    remitente_seleccionado,
    asunto_busqueda
)


st.dataframe(
    df_ultimos,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# 📈 HISTORIAL DE EJECUCIONES DEL ETL
# ============================================================

st.subheader("📈 Historial de ejecuciones del ETL")

df_historial = obtener_historial_etl()

if not df_historial.empty:

    st.dataframe(
        df_historial,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No existen ejecuciones registradas."
    )




# ============================================================
# 📊 RESULTADO DE LAS EJECUCIONES
# ============================================================

st.subheader("📊 Resultado de las ejecuciones")


if not df_historial.empty:

    df_grafico = df_historial.copy()

    # Convertir estado a texto para mostrarlo correctamente
    df_grafico["resultado"] = df_grafico["estado"].map({
        "OK": "OK",
        "ERROR": "ERROR"
    })


    fig_estado = px.scatter(
        df_grafico,
        x="fecha_ejecucion",
        y="resultado",
        color="estado",
        hover_data=[
            "id_ejecucion",
            "correos_encontrados",
            "correos_existentes",
            "correos_nuevos"
        ],
        title="Estado de las ejecuciones del ETL",
        labels={
            "fecha_ejecucion": "Fecha de ejecución",
            "resultado": "Resultado",
            "estado": "Estado"
        }
    )


    fig_estado.update_yaxes(
        categoryorder="array",
        categoryarray=["ERROR", "OK"]
    )


    st.plotly_chart(
        fig_estado,
        use_container_width=True
    )


else:

    st.info(
        "No existen ejecuciones registradas para mostrar."
    )