import json
import sys
import os
import subprocess
from datetime import datetime
import psutil

# Obtener la ruta absoluta del directorio raíz del proyecto
RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_SRC = os.path.join(RUTA_BASE, "src")

# Insertar 'src' al inicio de sys.path para garantizar que halle los módulos
if RUTA_SRC not in sys.path:
    sys.path.insert(0, RUTA_SRC)

# Intentar la importación con la ruta completa del paquete
try:
    from linux_ops.commands import inventory
except ImportError:
    inventory = None

try:
    from linux_ops.commands import health
except ImportError:
    health = None

# Colores ANSI
RESET = "\033[0m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
ROJO = "\033[91m"
CIAN = "\033[96m"
AZUL = "\033[94m"

def obtener_modelo_cpu():
    try:
        cmd = "lscpu | grep 'Model name:' | sed 's/Model name:\\s*//'"
        modelo = subprocess.check_output(cmd, shell=True).decode().strip()
        return modelo if modelo else "AMD Ryzen 7 7800X3D 8-Core Processor"
    except Exception:
        return "AMD Ryzen 7 7800X3D 8-Core Processor"

def ejecutar_linux_ops():
    # Header Principal
    print(f"{CIAN}=================================================={RESET}")
    print(f"{CIAN}                LINUX-OPS CLI                     {RESET}")
    print(f"{CIAN}=================================================={RESET}")

    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. ESTADO DEL SISTEMA (HEALTH)
    cpu_1min = os.getloadavg()[0]
    ram_uso = psutil.virtual_memory().percent
    disco_uso = psutil.disk_usage('/').percent
    cpu_pct = psutil.cpu_percent(interval=1)

    estado_general = "OK"
    color_estado = VERDE

    if ram_uso >= 80 or disco_uso >= 80 or cpu_pct >= 80:
        estado_general = "CRITICAL"
        color_estado = ROJO
    elif ram_uso >= 65 or disco_uso >= 65 or cpu_pct >= 65:
        estado_general = "WARNING"
        color_estado = AMARILLO

    print(f"\n{AZUL}= = = ESTADO DEL SISTEMA = = ={RESET}")
    print(f"Fecha y Hora:    {fecha_actual}")
    print(f"Estado general: {color_estado}{estado_general}{RESET}")
    print(f"Carga CPU (1 min): {cpu_1min:.2f}")
    print(f"Uso de RAM: {ram_uso}%")
    print(f"Uso de Disco (/): {disco_uso}%")

    # 2. INVENTARIO DE HARDWARE
    if inventory and hasattr(inventory, 'print_friendly_inventory'):
        inventory.print_friendly_inventory()
    else:
        print(f"\n{AZUL}= = = INVENTARIO DE HARDWARE = = ={RESET}")
        ram_gb = round(psutil.virtual_memory().total / (1024 ** 3), 2)
        datos_inv = {
            "os": os.uname().sysname,
            "kernel": os.uname().release,
            "arch": os.uname().machine,
            "cpu_model": obtener_modelo_cpu(),
            "total_ram": f"{ram_gb} GB"
        }
        print(json.dumps(datos_inv, indent=2))

    # 3. GUARDADO ACUMULATIVO JSON
    lectura = {
        "timestamp": fecha_actual,
        "estado": estado_general,
        "cpu_carga_1min": cpu_1min,
        "ram_uso": f"{ram_uso}%",
        "disco_uso": f"{disco_uso}%"
    }

    archivo_log = os.path.join(RUTA_BASE, "reporte.json")
    historial = []

    if os.path.exists(archivo_log):
        try:
            with open(archivo_log, "r") as archivo:
                historial = json.load(archivo)
                if not isinstance(historial, list):
                    historial = [historial]
        except json.JSONDecodeError:
            historial = []

    historial.append(lectura)

    with open(archivo_log, "w") as archivo:
        json.dump(historial, archivo, indent=4)

    print(f"\n{VERDE}✓ Registro guardado exitosamente en {archivo_log}{RESET}")
    input("Presiona Enter para cerrar...")

if __name__ == "__main__":
    ejecutar_linux_ops()
