import json
import sys
from datetime import datetime
import psutil

print ( "= = = LINUX-OPS CLI = = =" )


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

# 1. Creamos la estructura de datos
datos_sistema = {
    "timestamp": fecha_actual,
    "estado": estado_sistema,
    "cpu_uso": f"{cpu_val}%",
    "ram_uso": f"{ram_val}%"
}

print ( " Datos recolectados:", datos_sistema )

# 2. Guardamos el diccionario dentro de un archivo JSON

if "--json" in sys.argv:
    with open ( "reporte.json", "w" ) as archivo:
        json.dump ( datos_sistema, archivo, indent=4 )

    print ( "¡Reporte guardado exitosamente en reporte.json!" )
else:
    print ( "Tip: Usa '--json' para exportar los resultados a un archivo." )


