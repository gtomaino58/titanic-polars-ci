# Titanic – Práctica de Computación en Sistemas Distribuidos

Análisis del dataset Titanic utilizando **Python puro (sin pandas)** y la librería **Polars**, desarrollado como programa ejecutable (no Jupyter Notebook), cumpliendo las restricciones de la práctica.

El proyecto genera automáticamente:

- Tablas en formato CSV  
- Gráficos en formato PNG  
- Informe automático (`INFORME_FINAL.md`)  
- Informe narrativo final (`Practica_Titanic_Informe_Final.txt`)  

Además, dispone de integración continua (GitHub Actions) y despliegue automático en GitHub Pages.

## Cómo ejecutar el proyecto

Desde la raíz del repositorio:

```bash
pip install -r requirements.txt
python -m src.main

Esto genera:

outputs/
    tables/
    figures/
INFORME_FINAL.md

** Tecnologías utilizadas

Python 3.11
Polars (en lugar de pandas)
Matplotlib
SciPy (para estimación de densidad KDE)
GitHub Actions (CI)
GitHub Pages (publicación automática)

** Estructura del proyecto

src/
    main.py
    ejercicio1.py
    ejercicio2.py
    plots.py
    io_utils.py
    tools/
        csv_to_html.py
        make_figures_index.py
        make_tables_index.py

data/
    titanic.csv
    pasajeros.csv
    supervivientes.csv

.github/workflows/
    ci.yml

** Ejercicio 1 – Titanic clásico

Incluye:

Exploración inicial (head, columnas, info)
Recuento por clase y sexo
Supervivencia por clase y sexo (pivot correcto)
Distribución de edades:
Histograma + densidad
Histograma alternativo
Tratamiento de valores nulos en edad
Identificación de menores de 16 años

** Ejercicio 2 – Join y análisis adicional

Unión (inner join) de pasajeros y supervivientes
Diagnóstico de calidad del join
Recuento por puerto de embarque
Edad media por sexo y supervivencia
Muertes por rango de edad
Muertes por clase y género

** Publicación automática

Cada git push:

Ejecuta el pipeline completo.
Genera los resultados.
Construye el sitio en site/.
Publica automáticamente en GitHub Pages.

Sitio web:
https://gtomaino58.github.io/titanic-polars-ci/

