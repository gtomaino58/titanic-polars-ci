# Titanic – Práctica de Computación en Sistemas Distribuidos

Análisis del dataset Titanic utilizando **Python puro (sin pandas)** y la librería **Polars**, desarrollado como programa ejecutable (no Jupyter Notebook), cumpliendo las restricciones de la práctica.

El proyecto genera automáticamente:

- Tablas en formato CSV  
- Gráficos en formato PNG  
- Informe automático (`INFORME_FINAL.md`)  
- Informe narrativo final (`Practica_Titanic_Informe_Final.txt`)  

Además, dispone de integración continua (GitHub Actions) y despliegue automático en GitHub Pages.

---

## Cómo ejecutar el proyecto

Desde la raíz del repositorio:

```bash
pip install -r requirements.txt
python -m src.main
