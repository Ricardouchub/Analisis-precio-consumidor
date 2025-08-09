# Analisis de precios al consumidor en Chile con Dashboard (2020-2025)

Este repositorio contiene el código y los datos para un dashboard interactivo que analiza los precios de la canasta básica en Chile. El proyecto utiliza un conjunto de datos públicos de la **Oficina de Estudios y Políticas Agrarias (ODEPA)**, que comprende más de 1.8 millones de registros recopilados entre 2020 y 2025.

<img width="744" height="339" alt="image" src="https://github.com/user-attachments/assets/2ccc3da9-cec2-4208-bfd1-c5a7719d5a5d" />



El objetivo principal de este proyecto es transformar un gran volumen de datos tabulares en una herramienta de visualización intuitiva. El dashboard permite a los usuarios explorar tendencias de precios, comparar costos entre regiones y canales de venta, y descubrir patrones estacionales de los alimentos más importantes para los consumidores en Chile.

---
## Procesamiento de Datos y Análisis

Antes del desarrollo del dashboard, se realizó un riguroso proceso de preparación y análisis de los datos.

### **1. Limpieza y Consolidación de Datos**
El proceso inicial se centró en unificar y estandarizar los 6 archivos CSV originales:
* **Consolidación:** Se combinaron todos los archivos en un único DataFrame de más de 1.8 millones de filas.
* **Estandarización:** Se limpiaron los nombres de las columnas (minúsculas, sin espacios ni tildes).
* **Corrección de Tipos:** Las columnas de fecha se convirtieron a formato `datetime` y las de precios a `float`, corrigiendo el uso de la coma como separador decimal.
* **Validación:** Se verificó la inexistencia de filas duplicadas y se analizaron los valores únicos de las columnas categóricas para asegurar la consistencia de los datos.

### **2. Análisis Exploratorio de Datos (EDA)**
Una vez con los datos limpios, se realizaron varios análisis para extraer insights clave:
* **Evolución Temporal:** Se analizó la inflación de productos clave como el pan, el aceite y la carne a través de gráficos de líneas.
* **Comparativa Geográfica:** Se compararon los niveles de precios entre las distintas regiones de Chile.
* **Análisis de Canales:** Se estudió la diferencia de precios entre supermercados, ferias libres y otros puntos de venta.
* **Estacionalidad:** Se identificaron los productos con mayores variaciones de precio entre el verano y el invierno.

### **3. Optimización para Despliegue**
Debido al gran tamaño del dataset, el archivo CSV final fue convertido a formato **Parquet** y se optimizaron los tipos de datos de las columnas de texto a `category`. Esto resultó en una **reducción drástica del consumo de memoria**, lo que fue crucial para poder desplegar la aplicación en un entorno web.

---
## Características del Dashboard

* **Filtros Interactivos:** Permite filtrar los datos por rango de años, múltiples regiones, canales de venta y productos específicos.
* **Visualización de Tendencias:** Un gráfico de líneas dinámico muestra la evolución de los precios de los productos seleccionados a lo largo del tiempo.
* **Análisis Comparativo:** Dos gráficos resumen la información de la selección:
    * **Comparativa Regional:** Muestra qué regiones son más caras o baratas en comparación con el promedio nacional.
    * **Distribución por Canal:** Un gráfico de torta revela la proporción de datos registrados en cada punto de monitoreo.
* **Interfaz Limpia:** Desarrollado con un diseño claro y profesional para una experiencia de usuario amigable.

---
## Ejecución Local

Para ejecutar este dashboard en tu propia máquina, sigue estos pasos:

1.  **Clona el repositorio:**
    ```bash
    git clone [https://github.com/Ricardouchub/Analisis-precio-consumidor.git](https://github.com/Ricardouchub/Analisis-precio-consumidor.git)
    cd Analisis-precio-consumidor
    ```

2.  **Configura Git LFS:** Este proyecto usa Git LFS para manejar el archivo de datos grande. Asegúrate de tenerlo instalado.
    ```bash
    git lfs install
    git lfs pull
    ```

3.  **Crea un entorno virtual e instala las dependencias:**
    ```bash
    # Crear entorno (opcional pero recomendado)
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate

    # Instalar librerías
    pip install -r requirements.txt
    ```

4.  **Ejecuta la aplicación:**
    ```bash
    python app.py
    ```

5.  Abre tu navegador y ve a la dirección `http://127.0.0.1:8050/` para ver el dashboard.

---
## Fuente de Datos

Los datos utilizados en este proyecto son de dominio público y fueron obtenidos del portal de datos abiertos de la [Oficina de Estudios y Políticas Agrarias (ODEPA)](https://datos.odepa.gob.cl/dataset/precios-consumidor) del Gobierno de Chile.

---
## Visualizaciones destacadas
<img width="894" height="524" alt="image" src="https://github.com/user-attachments/assets/8b67af09-e559-47ab-bbaa-b1fe698dab18" />
<img width="894" height="472" alt="image" src="https://github.com/user-attachments/assets/d7f2f0b2-9b99-4c83-b846-720f2b559589" />
<img width="879" height="586" alt="image" src="https://github.com/user-attachments/assets/87b470a5-17a4-4857-954d-aee753563dea" />



