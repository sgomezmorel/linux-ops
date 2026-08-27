import json
import platform

def get_cpu_model():
    # Leemos /proc/cpuinfo para buscar el modelo del procesador
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if "model name" in line:
                    # Formato en la linea: "model name : AMD Ryzen..."
                    return line.split(":")[1].strip()
    except Exception:
        return "Desconocido"
    return "Desconocido"

def get_total_ram():
    # Leemos /proc/meminfo para buscar la memoria RAM total
    try:
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if "MemTotal" in line:
                    # Formato en la linea: "MemTotal: 16384000 kB"
                    kb = int(line.split(":")[1].split()[0])
                    gb = round(kb / (1024 * 1024), 2)
                    return f"{gb} GB"
    except Exception:
        return "Desconocido"
    return "Desconocido"

def get_inventory():
    info = {
        "os": platform.system(),
        "kernel": platform.release(),
        "arch": platform.machine(),
        "cpu_model": get_cpu_model(),
        "total_ram": get_total_ram()
    }
    print(json.dumps(info, indent=2))

if __name__ == '__main__':
    get_inventory()
