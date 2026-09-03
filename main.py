import json
import sys
import os
import subprocess
from datetime import datetime, timedelta
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

def obtener_uptime():
    """Calcula el tiempo de actividad del sistema en dias, horas y minutos."""
    tiempo_boot = datetime.fromtimestamp(psutil.boot_time())
    tiempo_activo = datetime.now() - tiempo_boot

    dias = tiempo_activo.days
    horas, rem = divmod(tiempo_activo.seconds, 3600)
    minutos, _= divmod(rem, 60)

    partes = []
    if dias > 0:
        partes.append(f"{dias}d")
    if horas > 0 or dias >  0:
        partes.append(f"{horas}h")
    partes.append(f"{minutos}m")

    return " ".join(partes)

def obtener_top_procesos(limite=3):
    """Devuelve los procesos que más memoria RAM consumen actualmente."""
    procesos = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            procesos.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Ordenar de mayor a menor consumo de RAM
    procesos_ordenados = sorted(procesos, key=lambda x: x['memory_percent'] or 0, reverse=True)
    return procesos_ordenados[:limite]

def obtener_modelo_cpu():
    try:
        cmd = "lscpu | grep 'Model name:' | sed 's/Model name:\\s*//'"
        modelo = subprocess.check_output(cmd, shell=True).decode().strip()
        return modelo if modelo else "AMD Ryzen 7 7800X3D 8-Core Processor"
    except Exception:
        return "AMD Ryzen 7 7800X3D 8-Core Processor"

def obtener_trafico_red():
    """Devuelve los MB recibidos y enviados por la red."""
    io_red = psutil.net_io_counters()
    bytes_enviados = io_red.bytes_sent / (1024 * 1024) # Bytes a MB
    bytes_recibidos = io_red.bytes_recv / (1024 * 1024)
    return round (bytes_recibidos, 1), round(bytes_enviados, 1)

def obtener_puertos_en_escucha():
    puertos = []
    try:
        resultado = subprocess.run(
            ["sudo", "ss", "-tulnp"],
            capture_output=True,
            text=True
        )
        lineas = resultado.stdout.splitlines()[1:]

        for linea in lineas:
            partes = linea.split()
            if len(partes) >= 5:
               proto = partes[0].upper()
               direccion_local = partes[4]
               puerto = direccion_local.split(":")[-1]

               proceso = "Desconocido"
               if len(partes) >= 7:
                  proceso_info = partes[6]
                  if '="' in proceso_info:
                      proceso = proceso_info.split('="')[1].split('"')[0]

               if puerto.isdigit():
                   puerto.append((int(puerto), proto, proceso))
    except Exception:
        pass

    if not puertos:
        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == psutil.CONN_LISTEN:
                    puerto = conn.laddr.port
                    proto = "TCP" if conn.type == 1 else "UDP"
                    proc = "Protegido/Sistema"
                    if conn.pid:
                        try:
                            proc = psutil.Process(conn.pid).name()
                        except Exception:
                            pass
                    puertos.append((puerto, proto, proc))
        except Exception:
            pass

    puertos_unicos = list({(p[0], p[1]): p for p in puertos}.values())
    return sorted(puertos_unicos, key=lambda x: x[0])

    # Ordenamos por numero de puerto
    return sorted(puertos, key=lambda x: x[0])

def ejecutar_linux_ops():
    archivo_log = os.path.join(RUTA_BASE, "reporte.json")
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Muestreo de métricas
    cpu_1min = os.getloadavg()[0]
    ram_uso = psutil.virtual_memory().percent
    disco_uso = psutil.disk_usage('/').percent
    cpu_pct = psutil.cpu_percent(interval=1)

    uptime_str = obtener_uptime()
    usuarios_activos = len(psutil.users())
    top_proc = obtener_top_procesos(3)
    mb_recibidos, mb_enviados = obtener_trafico_red()
    puertos_escucha = obtener_puertos_en_escucha()

    # Agregar debajo de la IP de Red:
    # Evaluación del Estado del Sistema
    if ram_uso >= 80 or disco_uso >= 80 or cpu_pct >= 80:
        estado_general = "CRITICAL"
        color_estado = ROJO
    elif ram_uso >= 65 or disco_uso >= 65 or cpu_pct >= 65:
        estado_general = "WARNING"
        color_estado = AMARILLO
    else:
        estado_general = "OK"
        color_estado = VERDE

    # ENCABEZADO
    print(f"\n{CIAN}=================================================={RESET}")
    print(f"{CIAN}                LINUX-OPS CLI                     {RESET}")
    print(f"{CIAN}=================================================={RESET}")
    print(f" ⏱️  Fecha y Hora:    {fecha_actual}")
    print(f" ⏳ Uptime:          {uptime_str} (Usuarios activos: {usuarios_activos})")
    print(f" 📊 Estado general: {color_estado}{estado_general}{RESET}  (Carga CPU 1m: {cpu_1min:.2f})")

    # --- SECCIÓN DE RED Y CONECTIVIDAD ---
    net_io = psutil.net_io_counters()
    bytes_recv_mb = round(net_io.bytes_recv / (1024 * 1024), 1)
    bytes_sent_mb = round(net_io.bytes_sent / (1024 * 1024), 1)

    print(f"\n{AZUL}= = = RED Y CONECTIVIDAD = = ={RESET}")
    print(f"  📊 Trafico de Red:   ⬇️  {bytes_recv_mb} MB recibidos  |  ⬆️  {bytes_sent_mb} MB enviados")

    print(f"\n{AZUL}= = = AUDITORÍA DE SEGURIDAD (PUERTOS EN ESCUCHA) = = ={RESET}")

    if puertos_escucha:
        for puerto, proto, proc, pid in puertos_escucha:
            pid_str = f"PID: {pid}" if pid else "PID: N/A"
            print(f"  • Puerto {puerto:<5} [{proto}] | Servicio/Proceso: {proc}")
    else:
        print("  • No se detectaron puertos en escucha activos en la red.")

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

    print(f"\n🔥TOP 3 PROCESOS (MAYOR USO DE RAM):")
    for p in obtener_top_procesos(3):
        nombre = p['name'] if p['name'] else "Desconocido"
        ram_pct = p['memory_percent'] if p['memory_percent'] else 0.0
        print(f"    • PID {p['pid']:<6} | {nombre:<22} | RAM: {ram_pct:.1f}%")

    # 3. GUARDADO ACUMULATIVO JSON
    lectura = {
        "timestamp": fecha_actual,
        "uptime": uptime_str,
        "usuarios_activos": usuarios_activos,
        "estado": estado_general,
        "cpu_carga_1min": cpu_1min,
        "ram_uso_pct": f"{ram_uso}%",
        "disco_uso_pct": f"{disco_uso}%",
        "red_mb_recibidos": mb_recibidos,
        "red_mb_enviados": mb_enviados,
        "top_procesos_ram": [
            {"pid": p['pid'], "nombre": p['name'], "ram_pct": round(p['memory_percent'] or 0, 1)}
            for p in top_proc
        ]
    }

    historial = []
    if os.path.exists(archivo_log):
        try:
            with open(archivo_log, "r", encoding="utf-8") as f:
                historial = json.load(f)
                if not isinstance(historial, list):
                    historial = [historial]
        except json.JSONDecodeError:
            historial = []

    historial.append(lectura)

    try:
        with open(archivo_log, "w", encoding="utf-8") as f:
            json.dump(historial, f, indent=4, ensure_ascii=False)

        print(f"\n{VERDE}✓ Registro actualizado exitosamente en {archivo_log}{RESET}\n")
    except Exception as err:
        print(f"\n{ROJO}Error al actualizar el registro: {err}{RESET}\n")

    input("Presiona Enter para cerrar...")

if __name__ == "__main__":
    ejecutar_linux_ops()
