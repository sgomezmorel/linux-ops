import platform
import subprocess
import psutil
import socket

# Códigos de color ANSI
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

def draw_bar(percent, width=15):
    """Genera una barra de progreso visual tipo [████░░░░] con color dinámico."""
    filled = int(width * percent / 100)
    empty = width - filled
    
    if percent < 60:
        color = GREEN
    elif percent < 85:
        color = YELLOW
    else:
        color = RED

    bar = f"{color}" + "█" * filled + f"{RESET}" + "░" * empty
    return f"[{bar}] {percent:.1f}%"

def get_cpu_model():
    """Obtiene el nombre del procesador buscando en múltiples fuentes."""
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if "model name" in line.lower() or "nombre del modelo" in line.lower():
                    return line.split(":")[1].strip()
    except Exception:
        pass

    try:
        output = subprocess.check_output("lscpu", shell=True, text=True)
        for line in output.split("\n"):
            if "model name" in line.lower() or "nombre del modelo" in line.lower():
                return line.split(":")[1].strip()
    except Exception:
        pass

    proc = platform.processor()
    return proc if proc else "Procesador Genérico x86_64"

def get_best_ip():
    """Detecta la IP local real probando una conexión de socket rápida."""
    # Método 1: Socket rápido para descubrir la interfaz con salida a red
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        if ip and not ip.startswith("127."):
            return ip
    except Exception:
        pass

    # Método 2: Recorrer todas las interfaces disponibles si el método 1 falla
    for iface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if str(addr.family) == 'AddressFamily.AF_INET':
                ip = addr.address
                if not ip.startswith("127."):
                    return ip

    return "Sin conexión"

def get_sys_info():
    cpu_model = get_cpu_model()

    # Memoria RAM
    ram = psutil.virtual_memory()
    ram_total_gb = round(ram.total / (1024**3), 1)
    ram_uso_pct = ram.percent

    # Disco principal
    disco = psutil.disk_usage('/')
    disco_total_gb = round(disco.total / (1024**3), 1)
    disco_libre_gb = round(disco.free / (1024**3), 1)
    disco_uso_pct = disco.percent

    return {
        "equipo": platform.node(),
        "sistema_operativo": platform.system(),
        "kernel": platform.release(),
        "arquitectura": "64 bits" if "64" in platform.machine() else "32 bits",
        "procesador": cpu_model,
        "ram": {
            "total_gb": ram_total_gb,
            "pct": ram_uso_pct,
            "bar": draw_bar(ram_uso_pct)
        },
        "disco": {
            "libre_gb": disco_libre_gb,
            "total_gb": disco_total_gb,
            "pct": disco_uso_pct,
            "bar": draw_bar(disco_uso_pct)
        },
        "direccion_ip": get_best_ip()
    }

def print_friendly_inventory():
    data = get_sys_info()
    print("\n📋 ============== HARDWARE Y SISTEMA BASE ============== ")
    print("-" * 55)
    print(f"💻 Nombre del equipo:    {data['equipo']}")
    print(f"🐧 Sistema Operativo:    {data['sistema_operativo']} ({data['arquitectura']})")
    print(f"⚙️ Versión de Kernel:    {data['kernel']}")
    print(f"🧠 Procesador (Cerebro): {data['procesador']}")
    print(f"⚡ Memoria RAM:          {data['ram']['bar']} ({data['ram']['total_gb']} GB total)")
    print(f"💾 Disco Principal:      {data['disco']['bar']} ({data['disco']['libre_gb']} GB libres de {data['disco']['total_gb']} GB)")
    print(f"🌐 Dirección IP (Red):   {data['direccion_ip']}")
    print("-" * 55)

if __name__ == "__main__":
    print_friendly_inventory()
