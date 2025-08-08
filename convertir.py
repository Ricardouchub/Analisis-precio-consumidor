# convertir.py (versión optimizada)
import pandas as pd

print("Leyendo el archivo CSV...")
df = pd.read_csv('data/precios_consumidor_limpio_2020-2025.csv')

print("Optimizando tipos de datos...")
# Convertimos columnas con texto repetitivo al tipo 'category'
columnas_categoricas = [
    'region', 'sector', 'tipo_de_punto_monitoreo', 
    'grupo', 'producto', 'unidad'
]

for col in columnas_categoricas:
    df[col] = df[col].astype('category')

# Verificamos el nuevo uso de memoria (lo verás en tu terminal)
print("\nUso de memoria ANTES de la optimización:")
print(df.memory_usage(deep=True).sum() / 1024**2, "MB")

df.info(memory_usage='deep')

print("\nUso de memoria DESPUÉS de la optimización:")
# Recalculamos con los nuevos tipos de datos
for col in columnas_categoricas:
    df[col] = df[col].astype('category')
print(df.memory_usage(deep=True).sum() / 1024**2, "MB")

df.info(memory_usage='deep')

print("\nConvirtiendo a formato Parquet optimizado...")
# Guardamos el nuevo archivo, sobreescribiendo el anterior
df.to_parquet('data/precios_limpio.parquet', engine='pyarrow')

print("\n¡Conversión optimizada completada!")