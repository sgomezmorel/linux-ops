import json
import sys
import os
from datetime import datetime
import psutil

# Definicion de colores ANSI para la consola
RESET = "\033[0m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
ROJO = "\033[91m"
CIAN = "\033[96m"

print ( f"{CIAN}= = = LINUX-OPS CLI = = ={RESET}" )


# Capturamos la fecha y hora actual exacta
fecha_actual = datetime.now().strftime ( "%Y-%m-%d %H:%M:%S" )

# Capturamos datos reales del harware medimos uso real del proce y la mem RAM
# interval=1 toma una muestra de uso de CPU durante 1 segundo
cpu_val = psutil.cpu_percent(interval=1)
ram_val = psutil.virtual_memory().percent

# Logica de deteccion de anomalias (Umbrales ajustados para la VM)
estado_sistema = "OK"

if cpu_val >= 80 or ram_val >= 80:
    estado_sistema = "CRITICAL"
elif cpu_val >= 65 or ram_val >= 65:
    estado_sistema = "WARNING"

# Creamos la estructura de datos
lectura_actual = {
    "timestamp": fecha_actual,
    "estado": estado_sistema,
    "cpu_uso": f"{cpu_val}%",
    "ram_uso": f"{ram_val}%"
}

print ( " Datos recolectados:", lectura_actual )

# Guardamos el diccionario dentro de un archivo JSON
if "--json" in sys.argv:
   archivo_log = "reporte.json"
   historial = []

   # Si el archivo ya eciste y tiene contenido, leemos el historial previo
   if os.path.exists ( archivo_log ):
       try:
           with open ( archivo_log, "r" ) as archivo:
               historial = json.load ( archivo )
               if not isinstance ( historial, list ):
                   historial = [ historial ]
       except json.JSONDecodeError:
           historial = []

   # Anexamos la nueva lectura a la lista
   historial.append ( lectura_actual )

   # Guardamos la lista completa de registros
   with open ( archivo_log, "w" ) as archivo:
       json.dump ( historial, archivo, indent=4 )

   print ( f"\n¡Lectura registrada acumulativamente en {archivo_log}!" )
else:
   print ( f"\nTip: Usa '--json' para exportar los resultados a un archivo." )
