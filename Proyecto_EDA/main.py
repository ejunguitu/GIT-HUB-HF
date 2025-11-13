import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from IPython.display import FileLink
from pathlib import Path


ruta = 'BBDD/Data_project/Balance_Export_Import/EU_Wheat_IMPORT_Data_SP.xlsx'
df_import = pd.read_excel(ruta, sheet_name='Wheat_IMPORT_2015-25')

ruta = 'BBDD/Data_project/Balance_Export_Import/HS_code.xlsx'
df_hs = pd.read_excel(ruta, sheet_name='HS_Code')

df_import['Description'] = df_import['Product Code (CN)'].map(df_hs.set_index('HS code')['Description '])
df_import['Item description'] = df_import['Product Code (CN)'].map(df_hs.set_index('HS code')['Item description'])

df_import['Total value €'] = df_import['Value in thousand euro']*1000
df_import['Total value €'] = df_import['Total value €'].round(2)

df_import['€/tonelada'] = df_import['Total value €'] / df_import['Quantity in tonnes (grain equivalent)']
df_import['€/tonelada'] = df_import['€/tonelada'].round(2)

df_import['€/kg'] = df_import['Total value €'] / (df_import['Quantity in tonnes (grain equivalent)'] * 1000)
df_import['€/kg'] = df_import['€/kg'].round(2)

df_grouped = df_import.groupby('Item description')['Quantity in tonnes (grain equivalent)'].sum().sort_values()

# Creamos un gráfico de barras horizontales

df_grouped.plot(kind='barh', color='#32CD32')
plt.xlabel('Quantity in tonnes (grain equivalent)')
plt.ylabel('Item description')
plt.title('Valor acumulado por HS Code')

img_dir = Path('img')
img_dir.mkdir(exist_ok=True)
ruta_img = img_dir / 'Valor_acumulado_HS_code.png'
plt.savefig(ruta_img, dpi=300, bbox_inches='tight')
plt.show()


#---------------------------
# Creamos un gráfico de dispersión: 

items = df_import['Item description'].unique()
greens = plt.cm.Greens(np.linspace(0.4, 0.9, len(items)))
color_map = {item: greens[i] for i, item in enumerate(items)}

plt.figure(figsize=(14,10))

color_map = {}
for i, item in enumerate(items):
    if item == "Los demás":
        color_map[item] = '#DFFF00'  
    else:
        color_map[item] = greens[i]

for item in items:
    subset = df_import[df_import['Item description'] == item].sort_values('Marketing Year')
    plt.scatter(
        subset['Marketing Year'],
        subset['Quantity in tonnes (grain equivalent)'],
        color=color_map[item],
        alpha=0.7,
        label=item)
    
plt.xlabel('Marketing Year')
plt.ylabel('Quantity in tonnes (grain equivalent)')
plt.title('Dispersión de volumen de toneladas importadas por Marketing Year y tipo')
plt.legend(title='Item description', bbox_to_anchor=(1.05, 1), loc='upper left');

ruta_img = img_dir / 'Gráfico_dispersión_ton_año_tipo.png'
plt.savefig(ruta_img, dpi=300, bbox_inches='tight')
plt.show()

df_cereales = df_import[df_import['Description'] == 'Cereales']
df_import2 = df_cereales[df_cereales['Item description'] == 'Los demás']

df_product_acumulado = df_import2.groupby('Product Code (CN)').agg(
    {
    'Item description': 'first',
    'Quantity in tonnes (grain equivalent)': 'sum',
    'Value in thousand euro': 'sum',
    })


df_product_acumulado['Quantity in tonnes (grain equivalent)'] = df_product_acumulado['Quantity in tonnes (grain equivalent)'].round(2)
df_product_acumulado['Value in thousand euro'] = df_product_acumulado['Value in thousand euro'].round(2)

df_product_acumulado

df_product_acumulado = df_import2.groupby(['Product Code (CN)', 'Item description'], as_index=False)['Quantity in tonnes (grain equivalent)'].sum()
df_product_acumulado = df_product_acumulado.sort_values(by='Quantity in tonnes (grain equivalent)', ascending=False)

# Utilizaremos un Pie chart para ver la distribución del volumen: 

plt.figure(figsize=(4,4))
num_colors = len(df_product_acumulado)
colors = plt.cm.Greens(np.linspace(0.4, 0.9, num_colors))

plt.pie(
    df_product_acumulado['Quantity in tonnes (grain equivalent)'],
    labels=df_product_acumulado['Product Code (CN)'],
    autopct='%1.1f%%',
    startangle=140,
    colors=colors)

plt.title('Tamaño en "%" del tipo trigo por volumen de toneladas importadas')
plt.show();

ruta_img = img_dir / 'Pie_distrib.tipos_ton.png'
plt.savefig(ruta_img, dpi=300, bbox_inches='tight')
plt.show();

# Utilizaremos un Pie chart para ver la distribución del volumen: 

plt.figure(figsize=(4,4))
num_colors = len(df_product_acumulado)
colors = plt.cm.Greens(np.linspace(0.4, 0.9, num_colors))

plt.pie(
    df_product_acumulado['Value in thousand euro'],
    labels=df_product_acumulado['Product Code (CN)'],
    autopct='%1.1f%%',
    startangle=140,
    colors=colors)

plt.legend(df_product_acumulado['Item description'],
           title="Item description",
           bbox_to_anchor=(1.05, 1),
           loc='upper left')
plt.title('Tamaño en "%" del tipo trigo por valor de las toneladas importadas en EUR')
plt.show(); 

ruta_img = img_dir / 'Pie_distrib.tipos_EUR.png'
plt.savefig(ruta_img, dpi=300, bbox_inches='tight')
plt.show(); 

df_acumulado = df_import2.groupby('Marketing Year')['Total value €'].sum()
df_acumulado

# Gráfico de barras vertical
plt.figure(figsize=(10, 6))
x = np.arange(len(df_acumulado))
y = df_acumulado.values.flatten()
plt.bar(x, y, color='#32CD32') 

coef = np.polyfit(x, y, 1)
trend = np.poly1d(coef)
plt.plot(x, trend(x), color='darkgreen', linewidth=2, linestyle='--', label='Tendencia')

df_acumulado.plot(kind='bar', color='#32CD32', ax=plt.gca())
plt.xlabel('Marketing Year')
plt.ylabel('Quantity in tonnes (grain equivalent)')
plt.title('Total toneladas importadas acumulado por Marketing Year')
plt.xticks(x, df_acumulado.index, rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.show(); 

ruta_img = img_dir / 'Gráfico_volumen_ton_year.png'
plt.savefig(ruta_img, dpi=300, bbox_inches='tight')
plt.show();

# Gráfico de barras vertical
plt.figure(figsize=(10, 6))
x = np.arange(len(df_acumulado))
y = df_acumulado.values.flatten()
plt.bar(x, y, color='#32CD32') 

coef = np.polyfit(x, y, 1)
trend = np.poly1d(coef)
plt.plot(x, trend(x), color='darkgreen', linewidth=2, linestyle='--', label='Tendencia')

df_acumulado.plot(kind='bar', color='#32CD32', ax=plt.gca())
plt.xlabel('Marketing Year')
plt.ylabel('Value in thousand euro')
plt.title('Total valor en miles de las importaciones acumulado por Marketing Year')
plt.xticks(x, df_acumulado.index, rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.show(); 

ruta_img = img_dir / 'Gráfico_volumen_EUR_year.png'
plt.savefig(ruta_img, dpi=300, bbox_inches='tight')
plt.show();

# Gráfico de línea
plt.figure(figsize=(10, 6))
plt.plot(x, y, color='#32CD32') 

plt.xlabel('Marketing Year')
plt.ylabel('Value in thousand euro')
plt.title('Evolución del valor en miles de las importaciones acumulado por Marketing Year')
plt.xticks(rotation=45)
plt.show(); 

ruta_img = img_dir / 'Gráfico_evoluc.volumen_EUR_year.png'
plt.savefig(ruta_img, dpi=300, bbox_inches='tight')
plt.show()

# Agrupamos los valores por Partner por toneladas importadas: 

df_pais = df_import2.groupby('Partner', as_index=False)[['Quantity in tonnes (grain equivalent)']].sum()
df_pais = df_pais.sort_values(by='Quantity in tonnes (grain equivalent)', ascending=False)
df_top5 = df_pais.head(5)
df_top5

plt.figure(figsize=(14, 7))
highlight = ['Ukraine', 'United Kingdom', 'Canada', 'Russia', 'United States of America']
default_color = '#B0B0B0'
highlight_color = '#32CD32'

# Scatter plot: X = Marketing Year, Y = Quantity, color por Partner
partners = df_import2['Partner'].unique()

for partner in partners:
    subset = df_import2[df_import2['Partner'] == partner]

    if partner in highlight:
        marker = 'D'
        color = highlight_color
        size = 100 
    else:
        marker = 'o'
        color = default_color
        size = 50

    plt.scatter(
        subset['Marketing Year'],
        subset['Quantity in tonnes (grain equivalent)'],
        color=color,
        alpha=0.7,
        label=partner,
        marker=marker,
        s=size)

plt.xlabel('Marketing Year')
plt.ylabel('Quantity in tonnes (grain equivalent)')
plt.title('Dispersión de cantidad por socio importador y Marketing Year')
plt.legend(title='Partner', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show();

ruta_img = img_dir / 'Gráfico_disp.sociobyyear.png'
plt.savefig(ruta_img, dpi=300, bbox_inches='tight')
plt.show();


df_filtrado = df_import2[df_import2['Quantity in tonnes (grain equivalent)'] > 100000]
plt.figure(figsize=(14, 7))

partners = df_filtrado['Partner'].unique()

for partner in partners:
    subset = df_filtrado[df_filtrado['Partner'] == partner]
    
    if partner == 'Ukraine':
        color = '#FFCC00'
        size = 100
    else:
        color = '#32CD32'
        size = 70
    
    # Scatter plot:
    plt.scatter(
        subset['Marketing Year'],
        subset['Quantity in tonnes (grain equivalent)'],
        color=color,
        alpha=0.7,
        s=size,
        label=partner)


handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), title='Partner', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.xlabel('Marketing Year')
plt.ylabel('Quantity in tonnes (grain equivalent)')
plt.title('Dispersión de cantidad segmento: > 100000 por Marketing Year y socio')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show(); 

ruta_img = img_dir / 'Gráfico_segmento1_sup.100mil.sociobyyear.png'
plt.savefig(ruta_img, dpi=300, bbox_inches='tight')
plt.show();


# Seleccionar top 5
df_top5 = df_pais.sort_values(by='Quantity in tonnes (grain equivalent)', ascending=False).head(5)

colors = []
num_partners = len(df_top5)
green_gradient = plt.cm.Greens(np.linspace(0.5, 0.9, num_partners))

for i, partner in enumerate(df_top5['Partner']):
    if partner == 'Ukraine':
        colors.append('#FFD700')
    else:
        colors.append(green_gradient[i])

# Pie chart:
plt.figure(figsize=(8, 8))
plt.pie(
    df_top5['Quantity in tonnes (grain equivalent)'].values, 
    autopct='%1.1f%%', 
    startangle=90, 
    colors=colors,
    textprops={'fontsize': 10})

plt.legend(
    df_top5['Partner'],
    title='Partner', 
    bbox_to_anchor=(1.05, 1), 
    loc='upper left', 
    fontsize=12, 
    title_fontsize=10)

plt.title(' 5 Socios importadores más representativos por toneladas importadas')
plt.axis('equal')
plt.tight_layout()
plt.show(); 

ruta_img = img_dir / 'Gráfico_pie_top5_socio.png'
plt.savefig(ruta_img, dpi=300, bbox_inches='tight')
plt.show();

df_resumen_anual = df_import2.groupby('Marketing Year', as_index=False)[['Value in thousand euro', 'Quantity in tonnes (grain equivalent)']].sum()
df_resumen_anual['Value in thousand euro'] = df_resumen_anual['Value in thousand euro'].round(2)
df_resumen_anual['Quantity in tonnes (grain equivalent)'] = df_resumen_anual['Quantity in tonnes (grain equivalent)'].round(2)
df_resumen_anual

palette_tech_agro = {
    'Value in thousand euro': '#228B22',
    'Quantity in tonnes (grain equivalent)': '#7CFC00'}

df_plot = df_resumen_anual.melt(
    id_vars='Marketing Year', 
    value_vars=['Value in thousand euro', 'Quantity in tonnes (grain equivalent)'],
    var_name='Tipo', 
    value_name='Valor')

plt.figure(figsize=(12,8))
sns.barplot(data=df_plot, x='Marketing Year', y='Valor', hue='Tipo', palette=palette_tech_agro)

plt.title('Valores acumulados anuales por Marketing Year - ton & eur')
plt.ylabel('Valor acumulado', fontsize=12)
plt.xlabel('Marketing Year', fontsize=10)  
plt.xticks(fontsize=8, rotation=45)
plt.legend(title='Tipo', title_fontsize=11, fontsize=9)
sns.despine()

plt.show(); 

ruta_img = img_dir / 'Gráfico_indicadores_acumulados.png'
plt.savefig(ruta_img, dpi=300, bbox_inches='tight')
plt.show();

df_filtrado = df_import2[df_import2['Quantity in tonnes (grain equivalent)'] > 100000]

ultimo_anio = df_filtrado['Month Date'].max()
primer_anio = ultimo_anio - pd.DateOffset(years=10)
df_ultimos10 = df_filtrado[df_filtrado['Month Date'].between(primer_anio, ultimo_anio)]

top5_partners = df_ultimos10.groupby('Partner')['Quantity in tonnes (grain equivalent)'] \
                            .sum() \
                            .sort_values(ascending=False) \
                            .head(5) \
                            .index.tolist()

df_top5 = df_ultimos10[df_ultimos10['Partner'].isin(top5_partners)]

pivot = df_top5.pivot_table(
    index='Marketing Year',
    columns='Partner',
    values='€/tonelada',
    aggfunc='mean')

cmap = sns.light_palette("green", as_cmap=True)
mask_ukraine = pivot.columns == 'Ukraine'

plt.figure(figsize=(12,6))
ax = sns.heatmap(
    pivot,
    annot=True,
    fmt=".2f",
    cmap=cmap,
    linewidths=0.5,
    linecolor='gray',
    cbar_kws={'label': '€/tonelada'})

for i, col in enumerate(pivot.columns):
    if col == 'Ukraine':
        for y in range(pivot.shape[0]):
            ax.add_patch(plt.Rectangle((i, y), 1, 1, fill=True, color="#FFD700", alpha=0.3))


plt.title('€/ton promedio por marketing year y Socio importador')
plt.xlabel('Partner', fontsize=12)
plt.ylabel('Marketing Year', fontsize=12)
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show(); 

ruta_img = img_dir / 'Gráfico_correlac.promedio_eur_ton.png'
plt.savefig(ruta_img, dpi=300, bbox_inches='tight')
plt.show();

# Vamos a depurar los datos de clima 2024 para utilizarlo como ejemplo: 
ruta = 'BBDD/Data_project/Clima_AEMET/2024/TM_MES_2024.csv'
df_clima_24 = pd.read_csv(ruta, sep=';', encoding='ISO-8859-1')
df_clima_24

df_clima_24 = df_clima_24.dropna(how='all')
df_media_mensual_24 = df_clima_24.mean(numeric_only=True)
df_temp_24 = df_media_mensual_24.reset_index()
df_temp_24.columns = ['Date', 'Temperatura_Media']
df_temp_24 = df_temp_24.drop(df_temp_24.index[[12, 13]])

df_temp_24['Date'] = pd.to_datetime(df_temp_24['Date'], format='%d/%m/%Y')

# Vamos a depurar los datos de clima 2023 para utilizarlo como ejemplo: 
ruta = 'BBDD/Data_project/Clima_AEMET/2023/TM_MES_2023.csv'
df_clima_23 = pd.read_csv(ruta, sep=';', encoding='ISO-8859-1')
df_clima_23 = df_clima_23.dropna(how='all')
df_media_mensual_23 = df_clima_23.mean(numeric_only=True)
df_temp_23 = df_media_mensual_23.reset_index()
df_temp_23.columns = ['Date', 'Temperatura_Media']
df_temp_23 = df_temp_23.drop(df_temp_23.index[[12, 13]])
df_temp_23['Date'] = pd.to_datetime(df_temp_23['Date'], format='%d/%m/%Y')

# Vamos a depurar los datos de clima 2022 para utilizarlo como ejemplo: 
ruta = 'BBDD/Data_project/Clima_AEMET/2022/TM_MES_2022.csv'
df_clima_22 = pd.read_csv(ruta, sep=';', encoding='ISO-8859-1')
df_clima_22 = df_clima_22.dropna(how='all')
df_media_mensual_22 = df_clima_22.mean(numeric_only=True)
df_temp_22 = df_media_mensual_22.reset_index()
df_temp_22.columns = ['Date', 'Temperatura_Media']
df_temp_22 = df_temp_22.drop(df_temp_22.index[[12, 13]])
df_temp_22['Date'] = pd.to_datetime(df_temp_22['Date'], format='%d/%m/%Y')

# Vamos a depurar los datos de clima 2021 para utilizarlo como ejemplo: 
ruta = 'BBDD/Data_project/Clima_AEMET/2021/TM_MES_2021.csv'
df_clima_21 = pd.read_csv(ruta, sep=';', encoding='ISO-8859-1')
df_clima_21 = df_clima_21.dropna(how='all')
df_media_mensual_21 = df_clima_21.mean(numeric_only=True)
df_temp_21 = df_media_mensual_21.reset_index()
df_temp_21.columns = ['Date', 'Temperatura_Media']
df_temp_21 = df_temp_21.drop(df_temp_21.index[[12, 13]])
df_temp_21['Date'] = pd.to_datetime(df_temp_21['Date'], format='%d/%m/%Y')


# Vamos a depurar los datos de clima 2020 para utilizarlo como ejemplo: 
ruta = 'BBDD/Data_project/Clima_AEMET/2020/TM_MES_2020.csv'
df_clima_20 = pd.read_csv(ruta, sep=';', encoding='ISO-8859-1')
df_clima_20 = df_clima_20.dropna(how='all')
df_media_mensual_20 = df_clima_20.mean(numeric_only=True)
df_temp_20 = df_media_mensual_20.reset_index()
df_temp_20.columns = ['Date', 'Temperatura_Media']
df_temp_20 = df_temp_20.drop(df_temp_20.index[[12, 13]])
df_temp_20['Date'] = pd.to_datetime(df_temp_20['Date'], format='%d/%m/%Y')


df_temperatura = [df_temp_20, df_temp_21, df_temp_22, df_temp_23, df_temp_24]
df_temp_20_24 = pd.concat(df_temperatura, ignore_index=True)
df_temp_20_24.head()


df_temp_20_24['Date'] = pd.to_datetime(df_temp_20_24['Date'], dayfirst=True)
df_temp_20_24 = df_temp_20_24.sort_values('Date')

verde_linea = '#2E8B57'
verde_puntos = '#66CDAA'
verde_relleno = '#C1E1C1'

# Gráfico de línea
plt.figure(figsize=(12,6))

plt.plot(
    df_temp_20_24['Date'], 
    df_temp_20_24['Temperatura_Media'],
    color=verde_linea, 
    marker='o', 
    markerfacecolor=verde_puntos, 
    linestyle='-', 
    linewidth=2, 
    markersize=6)

plt.fill_between(
    df_temp_20_24['Date'], 
    df_temp_20_24['Temperatura_Media'], 
    color=verde_relleno, 
    alpha=0.3)

plt.title('Temperaturas medias 2020-2024')
plt.xlabel('Fecha')
plt.ylabel('Temperatura Media (°C)')
plt.grid(True)
plt.tight_layout()
plt.show(); 

ruta_img = img_dir / 'Gráfico_data_AEMET_temp_med_20-24.png'
plt.savefig(ruta_img, dpi=300, bbox_inches='tight')
plt.show();



df_temp_20_24['Date'] = pd.to_datetime(df_temp_20_24['Date'], dayfirst=True)
df_temp_20_24['Año'] = df_temp_20_24['Date'].dt.year
df_temp_20_24['Mes'] = df_temp_20_24['Date'].dt.month

tabla = df_temp_20_24.pivot_table(
    values='Temperatura_Media', 
    index='Mes', 
    columns='Año',
    aggfunc='mean')

# Dibujamos el heatmap
plt.figure(figsize=(8,6))
sns.heatmap(
    tabla,
    annot=True,
    fmt=".1f",
    cmap=sns.diverging_palette(150, 10, s=80, l=50, as_cmap=True),
    linewidths=0.5,
    linecolor='gray')

plt.title('Mapa de calor de temperaturas medias 2020-2024')
plt.ylabel('Mes')
plt.xlabel('Año')
plt.show(); 

ruta_img = img_dir / 'Mapa_data_AEMET_temp_med_20-24.png'
plt.savefig(ruta_img, dpi=300, bbox_inches='tight')
plt.show();

