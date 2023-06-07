# -*- coding: utf-8 -*-
"""app

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JXtvbZmmNhFO8AuKRCYDQwsxDt_YRUPY
"""

# Cargar datos
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Utilizar la página completa en lugar de una columna central estrecha
st.set_page_config(layout="wide")

# Título principal
st.markdown("<h1 style='text-align: center; color: #4A148C;'>Enfermedades que han afectado gravemente a Nueva York 🗽</h1>", unsafe_allow_html=True)

# Cargar datos

df0 = pd.read_csv('covid.csv')  # base historico
df1 = pd.read_csv('vih.csv')  # base actual
df2 = pd.read_csv('causas_muertes.csv')  # base actual

# Tratamiento de datos
df0['fecha_muestra'] = pd.to_datetime(df0['fecha_muestra']) 
df0['fecha_muestra'] = df0['fecha_muestra'].apply(
    pd.to_datetime, format='%Y/%m/%d')
df0['año'] = df0['fecha_muestra'].dt.year
df1.columns = ['año', 'distritos', 'genero', 'edad', 'raza/etnia', 'diagnosticos_vih', 'tasa_diagnostico_vih',
               'diagnosticos_sida', 'tasa_diagnostico_sida', 'muertes']
df2.columns = ['año', 'causa_de_muerte', 'genero', 'raza/etnia',
               'muertes']
df2['raza/etnia'] = df2['raza/etnia'].replace(['Non-Hispanic White', 'Non-Hispanic Black','Asian and Pacific Islander','Other Race/ Ethnicity','Not Stated/Unknown' ], ['White Non-Hispanic', 'Black Non-Hispanic','Asian/Pacific Islander','Other/Unknown','Other/Unknown'])
a = df0.groupby(['año'])[['muertes']].sum().reset_index()
a.rename(columns={'muertes': 'muertes_covid'}, inplace=True)
b = df1.groupby(['año'])[['muertes']].sum().reset_index()
b.rename(columns={'muertes': 'muertes_VIH'}, inplace=True)
c = df2.groupby(['año'])[['muertes']].sum().reset_index()
c.rename(columns={'muertes': 'muertes_otras'}, inplace=True)
df = pd.merge(b, c, how='outer', on='año').merge(a, how='outer', on='año')

# Dividir el ancho en 3 columnas de igual tamaño
c1, c2, c3 = st.columns((1, 1, 1))

# --------------- Top sexo
c1.markdown("<h3 style='text-align: left; color: #000000;'> Top Muertes por Sexo </h3>",
            unsafe_allow_html=True)
base5 = df1.query('genero != "All"').groupby(df1['genero'])['muertes'].sum().reset_index()
base6 = df2.query('genero != "All"').groupby(df2['genero'])['muertes'].sum().reset_index()
df4 = pd.concat([base5, base6])

df5 = df4.groupby(df4['genero'])['muertes'].sum().reset_index().sort_values('muertes', ascending=False)
top_perp_name = (df5['genero'].value_counts().index[0])
top_perp_num = (round(df5['muertes'][1]/(df5['muertes'].sum()), 4)*100)

c1.text('Genero: '+str(top_perp_name)+', '+str(top_perp_num)+'%')

# --------------- Top raza
c2.markdown("<h3 style='text-align: left; color: #000000;'> Top Muertes por Raza </h3>", unsafe_allow_html=True)
base7 = df1.groupby(df1['raza/etnia'])['muertes'].sum().reset_index().sort_values('muertes', ascending=False)
base8 = df2.groupby(df2['raza/etnia'])['muertes'].sum().reset_index().sort_values('muertes', ascending=False)
df6 = pd.concat([base7, base8])
df7 = df6.groupby(df6['raza/etnia'])['muertes'].sum().reset_index().sort_values('muertes', ascending=False)
top_perp_name = (df7['raza/etnia'].value_counts().index[0])
top_perp_num = (round((df7['muertes'].max())/(df7['muertes'].sum()), 4)*100)

c2.text('Raza: '+str(top_perp_name)+', '+str(top_perp_num)+'%')

# --------------- Top edad
c3.markdown("<h3 style='text-align: left; color: #000000;'> Top Muertes por Edad </h3>",
            unsafe_allow_html=True)
base9 = df1.query('edad != "All"').groupby(df1['edad'])['muertes'].sum().reset_index()

top_perp_name = (base9['edad'].value_counts().index[5])
top_perp_num =  (round((base9['muertes'].max())/(base9['muertes'].sum()), 4)*100)

c3.text('Edad: '+str(top_perp_name)+', '+str(top_perp_num)+'%')

#---------------------------------SECCION 2--------------------------------------------------------------------------------------------------------------------------
st.markdown("<h2 style='text-align: center; color: #4A148C;'>Como ha afectado el VIH/SIDA a Nueva York 🗽</h2>", unsafe_allow_html=True)
#----- DONA1
# Filtrar las filas sin la categoría "all" en la columna "genero"
df_filtrado = df1[df1['genero'] != 'All']

# Agrupar por género y calcular la suma de diagnósticos de VIH por género
diagnosticos_vih_por_genero = df_filtrado.groupby('genero')['diagnosticos_vih'].sum()

# Calcular el total de diagnósticos de VIH por género
total_diagnosticos_vih = diagnosticos_vih_por_genero.sum()

# Crear un nuevo DataFrame para almacenar los resultados
df_porcentaje_vih = pd.DataFrame(columns=['Genero', 'Porcentaje'])

# Calcular el porcentaje de mujeres y hombres diagnosticados con VIH
porcentaje_mujeres_vih = (diagnosticos_vih_por_genero['Female'] / total_diagnosticos_vih) * 100
porcentaje_hombres_vih = (diagnosticos_vih_por_genero['Male'] / total_diagnosticos_vih) * 100

# Agregar los valores al DataFrame
df_porcentaje_vih.loc[0] = ['Mujeres', porcentaje_mujeres_vih]
df_porcentaje_vih.loc[1] = ['Hombres', porcentaje_hombres_vih]

# Agrupar por género y calcular la suma de diagnósticos de SIDA por género
diagnosticos_sida_por_genero = df_filtrado.groupby('genero')['diagnosticos_sida'].sum()

# Calcular el total de diagnósticos de SIDA por género
total_diagnosticos_sida = diagnosticos_sida_por_genero.sum()

# Crear un nuevo DataFrame para almacenar los resultados
df_porcentaje_sida = pd.DataFrame(columns=['Genero', 'Porcentaje'])

# Calcular el porcentaje de mujeres y hombres diagnosticados con VIH
porcentaje_mujeres_sida = (diagnosticos_sida_por_genero['Female'] / total_diagnosticos_sida) * 100
porcentaje_hombres_sida = (diagnosticos_sida_por_genero['Male'] / total_diagnosticos_sida) * 100

# Agregar los valores al DataFrame
df_porcentaje_sida.loc[0] = ['Mujeres', porcentaje_mujeres_sida]
df_porcentaje_sida.loc[1] = ['Hombres', porcentaje_hombres_sida]

# Calcular la suma de diagnósticos de VIH por año
diagnosticos_vih_por_año = df1.groupby('año')['diagnosticos_vih'].sum()

# Calcular la suma de diagnósticos de SIDA por año
diagnosticos_sida_por_año = df1.groupby('año')['diagnosticos_sida'].sum()

# Dividir el ancho en 3 columnas de igual tamaño
col1, col2 = st.columns(2)

# gráfica 1
fig1 = px.pie(df_porcentaje_vih, values='Porcentaje', names='Genero', title='<b>% Diagnosticos de VIH por genero <b>', hole=0.6)
fig1.update_traces(marker=dict(colors=['#BA68C8', '#9C27B0']))
fig1.update_layout(
    template='simple_white',
    title_x=0.5,
    annotations=[dict(text=str(total_diagnosticos_vih), x=0.5, y=0.5, font_size=22, showarrow=False)])
col1.plotly_chart(fig1)

# gráfica 2
fig2 = px.pie(df_porcentaje_sida, values='Porcentaje', names='Genero', title='<b>% Diagnosticos de SIDA por genero <b>', hole=0.6)
fig2.update_traces(marker=dict(colors=['#BA68C8', '#9C27B0']))
fig2.update_layout(
    template='simple_white',
    legend_title='Genero',
    title_x=0.5,
    annotations=[dict(text=str(total_diagnosticos_sida), x=0.5, y=0.5, font_size=22, showarrow=False)])
col1.plotly_chart(fig2)

# grafica 3
# debido a la cantidad de vatriables se resuekve crear dos gráficas una que muestre por año y la otra por genero

base2 = df1.groupby(['año'])[['diagnosticos_vih', 'diagnosticos_sida']].sum().reset_index()

d = base2[['año', 'diagnosticos_vih']].rename(columns={'diagnosticos_vih': 'valores'})
e = base2[['año', 'diagnosticos_sida']].rename(columns={'diagnosticos_sida': 'valores'})
d['categoria'] = 'VIH'
e['categoria'] = 'SIDA'
base2 = pd.concat([d, e])
base3 = base2.groupby(['categoria', 'año'])[['valores']].sum().reset_index()
# crear dataset
base1 = df1.query('genero != "All"').groupby(['genero'])[['diagnosticos_vih', 'diagnosticos_sida']].sum().reset_index()

# gráfica 4
fig = px.bar(base1, x='genero', y=['diagnosticos_vih', 'diagnosticos_sida'], barmode='group', color_discrete_map={
             'diagnosticos_vih': '#BA68C8', 'diagnosticos_sida': '#9C27B0'}, title='<b>Diagnosticos de VIH y SIDA por genero<b>')

# Agregar detalles a la gráfica
fig.update_layout(
    xaxis_title='Diagnóstico',
    yaxis_title='Diagnosticos',
    template='simple_white',
    title_x=0.5,
    legend_title='<b>Genero<b>')

# Mostrar gráfica utilizando Streamlit
col2.plotly_chart(fig)

# --------GRAFICA 5
# crear dataset
# crear gráfica
fig = px.bar(base3,  x='año', y='valores', color='categoria', barmode='group', color_discrete_map={
             'SIDA': '#BA68C8', 'VIH': '#9C27B0'}, title='<b>Diagnósticos de VIH y SIDA por año<b>')

# agregar detalles a la gráfica
fig.update_layout(
    xaxis_title='Año',
    yaxis_title='Diagnosticos',
    template='seaborn',
    title_x=0.5,
    legend_title='<b>Diagnóstico<b>')

col2.plotly_chart(fig)

col1, col2 = st.columns((1, 2))
# ----------------------------------------------------PREGUNTA 6------------------------------------------------------------
# ¿Como es la distribución en los diagnosticos de SIDA y los de VIH según la raza/etnia?
raza_etnia_sida = df1[df1['raza/etnia'] != 'Other/Unknown'].groupby('raza/etnia')['diagnosticos_sida'].sum()
raza_etnia_vih = df1[df1['raza/etnia'] != 'Other/Unknown'].groupby('raza/etnia')['diagnosticos_vih'].sum()

tabla_datos = pd.DataFrame({
    'raza/etnia': raza_etnia_sida.index,
    'diagnosticos_sida': raza_etnia_sida.values,
    'diagnosticos_vih': raza_etnia_vih.values
})

aids_diagnoses = tabla_datos['diagnosticos_sida'].values
labels = tabla_datos['raza/etnia'].values

# Crear la figura y los ejes
fig = px.pie(tabla_datos, values='diagnosticos_sida', names='raza/etnia', title='Distribución de diagnósticos de SIDA por raza')

# Graficar la torta de "AIDS diagnoses"
fig.update_traces(marker=dict(colors=['#7B1FA2', '#E1BEE7', '#CE93D8', '#AB47BC', '#8E24AA']))

# Mostrar las gráficas en Streamlit
col1.plotly_chart(fig)

hiv_diagnoses = tabla_datos['diagnosticos_vih'].values
labels = tabla_datos['raza/etnia'].values

# Crear la figura y los ejes
fig = px.pie(tabla_datos, values='diagnosticos_vih', names='raza/etnia', title='Distribución de diagnósticos de SIDA por raza')

# Graficar la torta de "AIDS diagnoses"
fig.update_traces(marker=dict(colors=['#7B1FA2', '#E1BEE7', '#CE93D8', '#AB47BC', '#8E24AA']))

# Mostrar las gráficas en Streamlit
col1.plotly_chart(fig)

# --------GRAFICA 6
# Crear dataset
estadisticas = df1.query('edad != "All"').groupby('edad')[['diagnosticos_vih', 'diagnosticos_sida']].mean().reset_index()

# Crear la figura y ejes para el gráfico de líneas
fig = px.line(estadisticas, x='edad', y=['diagnosticos_vih', 'diagnosticos_sida'], title='Promedio SIDA y VIH por rango de edad')

# Cambiar los colores de las líneas
fig.update_traces(line=dict(color='#BA68C8'), name='VIH')
fig.update_traces(line=dict(color='#9C27B0'), name='SIDA')

# Configurar los ejes y la leyenda
fig.update_xaxes(title='Edad')
fig.update_yaxes(title='Promedio')

# Mostrar el gráfico en Streamlit
col2.plotly_chart(fig)

#---------------------------------------------SECCION2--------------------------
#------------ GRAFICA 1
st.markdown("<h2 style='text-align: center; color: #000000;'>Como ha afectado el COVID-19 a Nueva York 🗽</h2>",
            unsafe_allow_html=True)

c1, c2 = st.columns((1, 1))
df0['mes_año'] = df0['fecha_muestra'].dt.strftime('%Y-%m')
base = df0.groupby('mes_año')[['confirmados_covid', 'muertes']].sum().reset_index()

# Convertir la columna 'mes_año' en una categoría con el orden correcto de los meses
base['mes_año'] = pd.to_datetime(base['mes_año'])
base['mes_año'] = base['mes_año'].dt.strftime('%Y-%m')
meses_ordenados = sorted(base['mes_año'].unique())

# Ordenar el DataFrame base por la columna 'mes_año'
base['mes_año'] = pd.Categorical(
    base['mes_año'], categories=meses_ordenados, ordered=True)
base = base.sort_values('mes_año')

x_pos = base['mes_año']

# Crear figura
fig = go.Figure()

# Agregar líneas para los promedios de confirmados y muertes
fig.add_trace(go.Scatter(x=x_pos, y=base['muertes'], mode='lines+markers', name='Muertes', line=dict(color='#BA68C8')))
fig.add_trace(go.Scatter(x=x_pos, y=base['confirmados_covid'], mode='lines+markers', name='Confirmados', line=dict(color='#9C27B0')))

# Configurar ejes y título del gráfico
fig.update_layout(
    title='Confirmados VS Muertes de COVID',
    xaxis=dict(title='Meses'),
    yaxis=dict(title='Casos'))

# Mostrar el gráfico en Streamlit
c1.plotly_chart(fig)

#-------DONA2

# Crear un nuevo DataFrame para almacenar los resultados
df_covid= pd.DataFrame(columns=['año', 'Porcentaje'])

# Agrupar por año y calcular la suma de las muertes
muertes_anio = df0.groupby('año')['muertes'].sum().reset_index()

# Calcular el total de muertes por año
total_muertes = muertes_anio['muertes'].sum()

# Crear un nuevo DataFrame para almacenar los resultados
df_covid= pd.DataFrame(columns=['año', 'Porcentaje'])

# Calcular el porcentaje de muertes por año
porcentaje_2020 = (muertes_anio['muertes'][0]/total_muertes) * 100
porcentaje_2021 = (muertes_anio['muertes'][1]/total_muertes) * 100

# Agregar los valores al DataFrame
df_covid.loc[0] = ['2020', porcentaje_2020]
df_covid.loc[1] = ['2021', porcentaje_2021]

# Hacer la gráfica 1
fig1 = px.pie(df_covid, values='Porcentaje', names='año', title='<b>% Muertes por covid segun el año <b>', hole=0.6)
fig1.update_traces(marker=dict(colors=['#BA68C8', '#9C27B0']))
fig1.update_layout(
    template='simple_white',
    title_x=0.5,
    annotations=[dict(text=str(total_muertes), x=0.5, y=0.5, font_size=22, showarrow=False)])

c1.plotly_chart(fig1)

# ------GRAAFICA 2

df0['dia_semana'] = df0['fecha_muestra'].dt.day_name()
promedio_por_dia = df0.groupby('dia_semana')[['confirmados_covid', 'hospitalizaciones']].mean()

# Obtener los nombres de los días de la semana y su posición en el eje x
dias_semana = promedio_por_dia.index
x_pos = range(len(dias_semana))

# Convertir el objeto range en una lista
x_pos_list = list(x_pos)

# Crear una figura y ejes para el gráfico de líneas
fig = go.Figure()

# Graficar las líneas de los promedios de confirmados y hospitalizaciones
fig.add_trace(go.Scatter(x=x_pos_list, y=promedio_por_dia['confirmados_covid'], mode='lines+markers', name='Confirmados', line=dict(color='#9C27B0')))
fig.add_trace(go.Scatter(x=x_pos_list, y=promedio_por_dia['hospitalizaciones'], mode='lines+markers', name='Hospitalizaciones', line=dict(color='#BA68C8')))

# Configurar etiquetas y título del gráfico
fig.update_layout(
    title='Promedio por día de la semana de confirmados y hospitalizaciones',
    xaxis=dict(title='Día de la semana'),
    yaxis=dict(title='Promedio')
)

# Mostrar el gráfico en Streamlit
c2.plotly_chart(fig)



# ----GRAFICA 3

# Agrupar los datos por día del mes y calcular la suma de 'examinados', 'hospitalizaciones' y 'muertes'
datos_por_dia = df0.groupby(df0['fecha_muestra'].dt.day)['diagnosticos_vih'].sum().reset_index()

# Calcular la tasa de mortalidad y la tasa de hospitalización por día del mes
datos_por_dia['tasa_mortalidad'] = (
    datos_por_dia['muertes'] / datos_por_dia['residentes_examinados']) * 100
datos_por_dia['tasa_hospitalizacion'] = (
    datos_por_dia['hospitalizaciones'] / datos_por_dia['residentes_examinados']) * 100

# Crear una figura y ejes para el gráfico de líneas
fig = go.Figure()

# Graficar las líneas de la tasa de mortalidad y la tasa de hospitalización
fig.add_trace(go.Scatter(x=datos_por_dia.index, y=datos_por_dia['tasa_mortalidad'], mode='lines+markers', name='Tasa de mortalidad', line=dict(color='#BA68C8')))
fig.add_trace(go.Scatter(x=datos_por_dia.index, y=datos_por_dia['tasa_hospitalizacion'], mode='lines+markers', name='Tasa de hospitalizaciones', line=dict(color='#9C27B0')))

# Configuraciones adicionales del gráfico
fig.update_layout(
    title='Tasa de mortalidad y tasa de hospitalizaciones por día del mes',
    xaxis=dict(title='Día del mes'),
    yaxis=dict(title='Tasa (%)')
)

# Mostrar el gráfico en Streamlit
c2.plotly_chart(fig)

#----------------------------------SECCION3------------------------------------
# ---TITULO
st.markdown("<h2 style='text-align: center; color: #00000;'>Como otras enfermedades han afectado a Nueva York 🗽</h2>",
            unsafe_allow_html=True)


c1.markdown("&nbsp;" * 800)
# ----------------------------------------------------PREGUNTA 9------------------------------------------------------------
# ¿cantidad de muertes por raza?

df2['raza/etnia'] = df2['raza/etnia'].replace(['Non-Hispanic White', 'Non-Hispanic Black', 'Asian and Pacific Islander', 'Other Race/ Ethnicity', 'Not Stated/Unknown'], [
                                              'White Non-Hispanic', 'Black Non-Hispanic', 'Asian/Pacific Islander', 'Other/Unknown', 'Other/Unknown'])
deaths_by_race = df2.groupby(
    'raza/etnia')['muertes'].sum().sort_values(ascending=True)

# Crear la figura y los ejes
fig = go.Figure()

# Generar una secuencia de colores para el degradado
num_colors = len(deaths_by_race)
colors = ['#7B1FA2', '#E1BEE7', '#8E24AA','#BA68C8', '#AB47BC', '#AB47BC', '#CE93D8']

# Crear el gráfico de barras horizontales con degradado de colores
fig.add_trace(go.Bar(
    y=deaths_by_race.index,
    x=deaths_by_race.values,
    orientation='h',
    marker=dict(color=colors),
))

# Configurar las etiquetas y el título del gráfico
fig.update_layout(
    title='Muertes por raza/etnicidad',
    xaxis=dict(title='Cantidad de muertes'),
    yaxis=dict(title='Raza/Etnicidad')
)

# Mostrar el gráfico de barras en Streamlit
st.plotly_chart(fig)


# ----------------------------------------------------PREGUNTA 8------------------------------------------------------------
# ¿Cual fue el top 5 de enfermedades que registró más muertes entre el 2015 y el 2019?

# crear un base para las variables que vamos a usar
base = df2[['año', 'causa_de_muerte', 'muertes']]
# Filtrar los últimos 5 años
df_filtrado = base[base['año'] >= 2010]
# Agrupar por año y causa de muerte
top_por_año = df_filtrado.groupby(['año', 'causa_de_muerte'])['muertes'].sum(
).reset_index().sort_values(by=['año', 'muertes'], ascending=[True, False])
# Obtener las tres primeras filas de cada grupo (año)
top_tres = top_por_año.groupby('año').head(5)

# cambiar el nombre de las enfermedades
# Crear un diccionario con los cambios de nombres
nombres = {'Diseases of Heart (I00-I09, I11, I13, I20-I51)': 'Enfermedades del Corazón',
           'Malignant Neoplasms (Cancer: C00-C97)': 'Neoplasmas malignos (Cáncer)',
           'All Other Causes': 'Todas las demás causas',
           'Influenza (Flu) and Pneumonia (J09-J18)': 'Influenza y neumonia',
           'Diabetes Mellitus (E10-E14)': 'Diabetes Mellitus',
           'Cerebrovascular Disease (Stroke: I60-I69)': 'Enfermedad cerebrovascular',
           'Chronic Lower Respiratory Diseases (J40-J47)': 'Enfermedades Crónicas de las Vías Respiratorias Inferiores'}

# Aplicar los cambios de nombres a la variable deseada
top_tres['causa_de_muerte'] = top_tres['causa_de_muerte'].replace(nombres)


# Obtener los años y enfermedades únicas
anios_unicos = top_tres['año'].unique()
enfermedades_unicas = top_tres['causa_de_muerte'].unique()
# Configurar el ancho de las barras
bar_width = 0.6 / len(enfermedades_unicas)

# Definir una lista de colores personalizados
colores = ['#7B1FA2', '#E1BEE7', '#8E24AA','#BA68C8', '#AB47BC', '#AB47BC', '#CE93D8']

# Crear la figura
fig = go.Figure()

# Generar las barras correspondientes a cada enfermedad
for i, enfermedad in enumerate(enfermedades_unicas):
    # Obtener las muertes correspondientes a la enfermedad y año
    muertes = top_tres[top_tres['causa_de_muerte'] == enfermedad].set_index('año')['muertes']

    # Crear una lista de muertes correspondiente a los años únicos
    muertes_actualizadas = [
        muertes[anio] if anio in muertes.index else 0 for anio in anios_unicos
    ]

    # Generar los valores de x para la enfermedad actual
    x = np.arange(len(anios_unicos)) + i * bar_width

    # Agregar la barra correspondiente a la enfermedad actual al gráfico
    fig.add_trace(
        go.Bar(
            x=x,
            y=muertes_actualizadas,
            name=enfermedad,
            width=bar_width,
            marker_color=colores[i % len(colores)]
        )
    )

# Configurar el diseño del gráfico
fig.update_layout(
    xaxis=dict(
        title='Año',
        tickmode='array',
        tickvals=np.arange(len(anios_unicos)),
        ticktext=anios_unicos
    ),
    yaxis=dict(title='Número de muertes'),
    title='Top 5 enfermedades con más muertes por año',
    legend=dict(
        title='Causas de muerte',
        orientation='h',
        yanchor="top",
        y=1.02,
        x=1
    )
)

# Mostrar el gráfico de barras en Streamlit
st.plotly_chart(fig)


# ----------------------------------------------------PREGUNTA 7------------------------------------------------------------
#  ¿Cuál fue la principal causa de muerte 'Non-Hispanic Black' y 'Non-Hispanic?

base3 = df2[df2['raza/etnia'].isin(['Black Non-Hispanic',
                                   'White Non-Hispanic'])]
base3 = base3.groupby(['año', 'raza/etnia'])[['muertes']].sum().reset_index()

fig = px.bar(base3, x='año', y='muertes', color='raza/etnia', barmode='group',
             title='<b>Muertes de no hispanos por año<b>', color_discrete_map={
                          'Black Non-Hispanic': '#BA68C8', 'White Non-Hispanic': '#9C27B0'})

# Ajustar el tamaño de la gráfica
fig.update_layout(
    height=500,  # Ajusta la altura deseada en píxeles
    width=1600,  # Ajusta el ancho deseado en píxeles
    xaxis_title='Año',
    yaxis_title='Muertes',
    template='simple_white',
    title_x=0.5,
    legend_title='<b>Raza/etnia<b>',
)

# Mostrar la gráfica en Streamlit
st.plotly_chart(fig)